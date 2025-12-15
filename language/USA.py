import re
import string

# 只有整句是下面这几个才跳过（大小写不敏感）
SKIP_WORDS_STRICT = {"SIL", "MUSIC", "NOISE", "OTHER"}

# fillers
FILLERS = re.compile(
    r"\b(UH|UHH|UM|EH|MM|HM|AH|HUH|HA|ER)\b",
    re.IGNORECASE
)

# 删除尖括号标签
ANGLE_REGEX = re.compile(r"<[^>]*>")

# 删除标点
PUNCT_REGEX = re.compile(
    rf"[{re.escape(string.punctuation)}]"
    r"|[\u3000-\u303F]"
    r"|[\u2000-\u206F]"
    r"|[\uFF00-\uFFEF]"
    r"|[\uFE30-\uFE4F]"
    r"|[\u2E00-\u2E7F]"
)

# 删除 COMMA / PERIOD / QUESTIONMARK / EXCLAMATIONPOINT （裸词）
REMOVE_TAG_WORDS = re.compile(
    r"\b(COMMA|PERIOD|QUESTIONMARK|EXCLAMATIONPOINT)\b",
    re.IGNORECASE
)

# 英文数字词 → 数字
WORD_DIGIT_MAP = {
    "ZERO": "0",
    "ONE": "1",
    "TWO": "2",
    "THREE": "3",
    "FOUR": "4",
    "FIVE": "5",
    "SIX": "6",
    "SEVEN": "7",
    "EIGHT": "8",
    "NINE": "9",
}

WORD_DIGIT_REGEX = re.compile(
    r"\b(ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)\b",
    re.IGNORECASE
)


def normalize(text: str):
    if not text:
        return ""

    # A）精确判断整句是否为垃圾词
    t = text.strip().upper()
    if t in SKIP_WORDS_STRICT:
        return None

    # B）统一大写
    text = t

    # C）删 fillers
    text = FILLERS.sub("", text)

    # D）删 <...>
    text = ANGLE_REGEX.sub("", text)

    # E）删裸词标点标签
    text = REMOVE_TAG_WORDS.sub("", text)

    # F）删标点
    text = PUNCT_REGEX.sub("", text)

    # G）英文数字词 → 数字（核心修复）
    text = WORD_DIGIT_REGEX.sub(
        lambda m: WORD_DIGIT_MAP[m.group(1).upper()],
        text
    )

    # H）收尾空格
    text = " ".join(text.split())

    return text
