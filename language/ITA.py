import re
import unicodedata

ITA_NUMBER_MAP = {
    "ZERO": "0",
    "UNO": "1",
    "DUE": "2",
    "TRE": "3",
    "QUATTRO": "4",
    "CINQUE": "5",
    "SEI": "6",
    "SETTE": "7",
    "OTTO": "8",
    "NOVE": "9",
}

def normalize(text: str) -> str:
    # 先执行 Unicode NFKC 规整
    text = unicodedata.normalize("NFKC", text)

    # ITA 数字词 → 阿拉伯数字（仅映射规则）
    for k, v in ITA_NUMBER_MAP.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)

    text = text.translate(ITA_NUMBER_MAP)

    # 删除括号类标注 [], (), {}
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 仅保留意大利语/英语字母、数字与空格
    italian_english_only_pattern = re.compile(
        r"[^"
        r"a-zA-Z"
        r"àèéìíîòóùú"
        r"ÀÈÉÌÍÎÒÓÙÚ"
        r"0-9"
        r"\s"
        r"]"
    )

    text = italian_english_only_pattern.sub("", text)

    # 折叠多余空格
    text = re.sub(r"\s+", " ", text).strip()

    # 全部转为大写
    text = text.upper()

    return text
