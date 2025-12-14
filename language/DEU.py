import re
import unicodedata


def normalize(text: str) -> str:
    # 使用 Unicode NFKC 做兼容分解与组合
    text = unicodedata.normalize("NFKC", text)

    # 删除方括号、小括号、大括号中的标注内容
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 数字字符映射为德语单词
    digit_map = {
        '0': 'null',
        '1': 'eins',
        '2': 'zwei',
        '3': 'drei',
        '4': 'vier',
        '5': 'fuenf',
        '6': 'sechs',
        '7': 'sieben',
        '8': 'acht',
        '9': 'neun'
    }
    text = text.translate(str.maketrans(digit_map))

    # 仅保留德语、英语字母以及空格
    german_english_only_pattern = re.compile(
        r"[^"
        r"a-zA-Z"
        r"äöüßÄÖÜ"
        r"\s"
        r"]"
    )

    text = german_english_only_pattern.sub("", text)

    # 规整多余空格
    text = re.sub(r"\s+", " ", text).strip()

    # 全部转换为大写，便于对齐
    text = text.upper()

    return text


if __name__ == "__main__":
    import sys

    ori_text = sys.argv[1]
    print(normalize(ori_text))
