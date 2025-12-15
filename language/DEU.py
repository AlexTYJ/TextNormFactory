import re
import unicodedata

# =========================
# 数字字符统一
# =========================

# 东阿拉伯 / 全角数字 → 阿拉伯数字
DIGIT_MAP = str.maketrans(
    "٠١٢٣٤٥٦٧٨٩０１２３４５６７８９",
    "01234567890123456789"
)

# =========================
# 德语数字词 → 阿拉伯数字（词级）
# =========================

GERMAN_NUMBER_MAP = {
    # 0–9
    "null": "0",
    "ein": "1",
    "eins": "1",
    "eine": "1",
    "zwei": "2",
    "drei": "3",
    "vier": "4",
    "fünf": "5",
    "sechs": "6",
    "sieben": "7",
    "acht": "8",
    "neun": "9",

    # 10–19
    "zehn": "10",
    "elf": "11",
    "zwölf": "12",
    "dreizehn": "13",
    "vierzehn": "14",
    "fünfzehn": "15",
    "sechzehn": "16",
    "siebzehn": "17",
    "achtzehn": "18",
    "neunzehn": "19",

    # 20–90
    "zwanzig": "20",
    "dreißig": "30",
    "vierzig": "40",
    "fünfzig": "50",
    "sechzig": "60",
    "siebzig": "70",
    "achtzig": "80",
    "neunzig": "90",

    # 大数（词级，不组合）
    "hundert": "100",
    "tausend": "1000",
}

GERMAN_NUMBER_REGEX = re.compile(
    r"\b(" + "|".join(GERMAN_NUMBER_MAP.keys()) + r")\b",
    flags=re.IGNORECASE,
)

# =========================
# 主 normalize
# =========================

def normalize(text: str) -> str:
    # Unicode 规整
    text = unicodedata.normalize("NFKC", text)

    # 数字字符统一
    text = text.translate(DIGIT_MAP)

    # 删除方括号 / 小括号 / 大括号中的标注
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}", "", text)

    # 德语数字词 → 阿拉伯数字（词级）
    text = GERMAN_NUMBER_REGEX.sub(
        lambda m: GERMAN_NUMBER_MAP[m.group(0).lower()],
        text,
    )

    # 仅保留德语 / 英语字母、数字、空格
    german_english_only_pattern = re.compile(
        r"[^"
        r"a-zA-Z"
        r"äöüßÄÖÜ"
        r"0-9"
        r"\s"
        r"]"
    )
    text = german_english_only_pattern.sub("", text)

    # 空格规整
    text = re.sub(r"\s+", " ", text).strip()

    # 全部大写（你原本的设计）
    text = text.upper()

    return text


if __name__ == "__main__":
    import sys
    print(normalize(sys.argv[1]))
