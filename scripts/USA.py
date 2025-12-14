import re

# 只有整句为下列几项时直接跳过（大小写不敏感）
SKIP_WORDS_STRICT = {"SIL", "MUSIC", "NOISE", "OTHER"}

# 填充词（美式发音犹豫）
FILLERS = re.compile(
    r"\b(UH|UHH|UM|EH|MM|HM|AH|HUH|HA|ER)\b",
    re.IGNORECASE
)

# 删除尖括号标签
ANGLE_REGEX = re.compile(r"<[^>]*>")

# 删除 COMMA / PERIOD / QUESTIONMARK / EXCLAMATIONPOINT（以单词形式给出的标记）
REMOVE_TAG_WORDS = re.compile(
    r"\b(COMMA|PERIOD|QUESTIONMARK|EXCLAMATIONPOINT)\b",
    re.IGNORECASE
)

digit_map_en = {
    "0": "ZERO", "1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR",
    "5": "FIVE", "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE",
}
DIGIT_REGEX = re.compile(r"[0-9]")


def normalize(text: str):
    if not text:
        return ""

    # A）精确判断整句是否为垃圾词（严格匹配）
    t = text.strip().upper()
    if t in SKIP_WORDS_STRICT:
        return None  

    # B）统一转成大写
    text = t

    # C）删除语气填充词
    text = FILLERS.sub("", text)

    # D）删除尖括号标签
    text = ANGLE_REGEX.sub("", text)

    # E）删除以单词拼写的标点标签
    text = REMOVE_TAG_WORDS.sub("", text)

    # F）数字转大写英文单词
    text = DIGIT_REGEX.sub(lambda m: digit_map_en[m.group(0)], text)

    # G）规整空格
    text = " ".join(text.split())

    return text
