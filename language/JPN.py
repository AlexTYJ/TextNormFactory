import re
import unicodedata


def normalize(text: str) -> str:
    # Unicode NFKC normalization
    text = unicodedata.normalize("NFKC", text)

    # Remove annotation inside [], (), {}
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 中文数字 → ASCII 数字
    digit_map = {
        "零": "0",
        "一": "1",
        "二": "2",
        "三": "3",
        "四": "4",
        "五": "5",
        "六": "6",
        "七": "7",
        "八": "8",
        "九": "9",
    }
    text = text.translate(str.maketrans(digit_map))

    # 仅保留：日文 + 英文 + 数字
    japanese_english_only_pattern = re.compile(
        r"[^"
        r"a-zA-Z0-9"
        r"\u3040-\u309F"      # 平假名
        r"\u30A0-\u30FF"      # 片假名
        r"\u31F0-\u31FF"
        r"\uFF65-\uFF9F"
        r"\u4E00-\u9FFF"
        r"\u3400-\u4DBF"
        r"\uF900-\uFAFF"
        r"\u3005\u3006\u3007"
        r"]"
    )

    text = japanese_english_only_pattern.sub("", text).replace("・", "")

    # 大写
    text = text.upper()

    # ======== 唯一新增的一句（CER 用）========
    text = " ".join([ch for ch in text if ch.strip() != ""])

    return text


if __name__ == "__main__":
    import sys
    print(normalize(sys.argv[1]))
