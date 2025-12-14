import regex as re

def normalize(text: str) -> str:
    """
    伊拉克阿拉伯语文本规范化：
    1. 移除变音符号。
    2. 处理 Hamza/Madda 及波斯字母变体。
    3. 将东阿数字映射为西阿数字。
    """
    # 移除重音符号（Fatha、Damma 等）
    diacritics = r'[\u064B-\u0652]'
    text = re.sub(diacritics, '', text)
    
    # 规范化 Hamza、Madda 及波斯字母
    text = re.sub('پ', 'ب', text)
    text = re.sub('ڤ', 'ف', text)
    text = re.sub(r'[آ]', 'ا', text)
    text = re.sub(r'[أإ]', 'ا', text)
    text = re.sub(r'[ؤ]', 'و', text)
    text = re.sub(r'[ئ]', 'ي', text)
    text = re.sub(r'[ء]', '', text)   

    # 东阿数字 → 西阿数字
    eastern_to_western_numerals = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', 
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    for eastern, western in eastern_to_western_numerals.items():
        text = text.replace(eastern, western)

    # 去除拉长符 (tatweel, U+0640)
    text = re.sub(r"\u0640", "", text)
    
    # 删除犹豫声（重复的 ا）
    text = re.sub(r"اا+", "", text)
    
    # 折叠多余空格
    text = re.sub(r'\s\s+', ' ', text)

    return text.strip()
