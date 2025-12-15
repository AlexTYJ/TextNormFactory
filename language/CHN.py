import re
import string

# 各类 Unicode 标点
PUNCT_REGEX = re.compile(
    rf"[{re.escape(string.punctuation)}]"
    r"|[\u3000-\u303F]"
    r"|[\u2000-\u206F]"
    r"|[\uFF00-\uFFEF]"
    r"|[\uFE30-\uFE4F]"
    r"|[\u2E00-\u2E7F]"
)

# 中文数字 → 阿拉伯数字 映射
digit_map_chn_to_arabic = {
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

# 只匹配“单个中文数字字符”
CHN_DIGIT_REGEX = re.compile(r"[零一二三四五六七八九]")

def normalize(text: str) -> str:
    # 去首尾空白
    text = text.strip()

    # 去标点
    text = PUNCT_REGEX.sub("", text)

    # 中文数字 → 阿拉伯数字
    text = CHN_DIGIT_REGEX.sub(
        lambda m: digit_map_chn_to_arabic[m.group(0)],
        text
    )

    return text
