import re

digit_map_chn = {
    "0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
    "5": "五", "6": "六", "7": "七", "8": "八", "9": "九",
}

DIGIT_REGEX = re.compile(r"[0-9]")

def normalize(text: str) -> str:
    text = text.strip()

    # 阿拉伯数字 → 中文数字
    text = DIGIT_REGEX.sub(lambda m: digit_map_chn[m.group(0)], text)

    return text
