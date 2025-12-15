import re
import unicodedata


def normalize(text: str) -> str:
    # Unicode NFKC normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove annotation inside [], (), {}
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 韩文数字 → ASCII 数字
    digit_map = {
        '영': '0', '일': '1', '이': '2', '삼': '3', '사': '4',
        '오': '5', '육': '6', '칠': '7', '팔': '8', '구': '9'
    }
    text = text.translate(str.maketrans(digit_map))

    # 仅保留：韩文 + 英文
    korean_english_only_pattern = re.compile(
        r"[^"
        r"\uAC00-\uD7A3"  # Hangul Syllables
        r"\u1100-\u11FF"  # Hangul Jamo
        r"\u3130-\u318F"  # Compatibility Jamo
        r"\uA960-\uA97F"
        r"\uD7B0-\uD7FF"
        r"a-zA-Z"
        r"]"
    )
    text = korean_english_only_pattern.sub("", text)

    # 大写
    text = text.upper()

    # ======== CER 用：字符级空格化（唯一新增）========
    text = " ".join([ch for ch in text if ch.strip() != ""])

    return text


if __name__ == "__main__":
    import sys
    print(normalize(sys.argv[1]))
