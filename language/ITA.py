import re
import unicodedata


def normalize(text: str) -> str:
    # 先执行 Unicode NFKC 规整
    text = unicodedata.normalize("NFKC", text)

    # 删除括号类标注 [], (), {}
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 数字映射为意大利语词形
    digit_map = {
        '0': 'zero',
        '1': 'uno',
        '2': 'due',
        '3': 'tre',
        '4': 'quattro',
        '5': 'cinque',
        '6': 'sei',
        '7': 'sette',
        '8': 'otto',
        '9': 'nove'
    }
    text = text.translate(str.maketrans(digit_map))

    # 仅保留意大利语/英语字母与空格
    italian_english_only_pattern = re.compile(
        r"[^"
        r"a-zA-Z"
        r"àèéìíîòóùú"
        r"ÀÈÉÌÍÎÒÓÙÚ"
        r"\s"
        r"]"
    )

    text = italian_english_only_pattern.sub("", text)

    # 折叠多余空格
    text = re.sub(r"\s+", " ", text).strip()

    # 全部转为大写
    text = text.upper()

    return text


if __name__ == "__main__":
    import sys

    ori_text = sys.argv[1]
    print(normalize(ori_text))
