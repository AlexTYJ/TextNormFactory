import re
import unicodedata


def normalize(text: str) -> str:
    # 使用 Unicode NFKC 做规整
    text = unicodedata.normalize("NFKC", text)

    # 删除括号内的标注 [], (), {}
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 数字映射为韩语读法
    digit_map = {
        '0': '영', '1': '일', '2': '이', '3': '삼', '4': '사',
        '5': '오', '6': '육', '7': '칠', '8': '팔', '9': '구'
    }
    text = text.translate(str.maketrans(digit_map))

    korean_english_only_pattern = re.compile(
        r"[^"
        r"\uAC00-\uD7A3"  # 谚文现代音节
        r"\u1100-\u11FF"  # 谚文字母 (Jamo)
        r"\u3130-\u318F"  # 谚文兼容符号
        r"\uA960-\uA97F"  # 谚文扩展 A
        r"\uD7B0-\uD7FF"  # 谚文扩展 B
        r"a-zA-Z"  # 英文字母
        r"]"
    )

    text = korean_english_only_pattern.sub("", text)

    text = text.upper()

    return text


if __name__ == "__main__":
    import sys

    ori_text = sys.argv[1]
    print(normalize(ori_text))
