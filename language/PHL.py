import re
import unicodedata
from typing import Dict, List


# ===============================
# 菲律宾语数字 → 阿拉伯数字 映射
# （唯一新增的映射规则）
# ===============================
FIL_NUMBER_MAP = {
    "ZERO": "0",
    "ISA": "1",
    "DALAWA": "2",
    "TATLO": "3",
    "APAT": "4",
    "LIMA": "5",
    "ANIM": "6",
    "PITO": "7",
    "WALO": "8",
    "SIYAM": "9",
}


def normalize(text: str) -> str:
    """
    菲律宾语完整规范化脚本（修正版）

    主要功能：
    1. 重复字母完全归约（sobrang → sobrang）
    2. 智能缩写展开（'yung → ang, d'yan → diyan）
    3. 外来词标准化（café → cafe, azúcar → asukal）
    4. 标点/空格清理
    5. URL/电子邮件保护
    """
    if not text.strip():
        return text

    # 预处理：保护URL/电子邮件
    protected_spans = []
    text = protect_special_content(text, protected_spans)

    # 处理顺序（重要！）
    text = remove_accents(text)                  # 先去重音
    text = reduce_repeated_characters(text)      # 再去重字母
    text = expand_contractions(text)             # 然后展开缩写
    text = standardize_spelling(text)            # 最后标准化拼写

    # ===============================
    # 菲律宾语数字词 → 阿拉伯数字
    # （仅映射规则）
    # ===============================
    for k, v in FIL_NUMBER_MAP.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)

    # 后处理
    text = restore_protected_content(text, protected_spans)
    text = clean_text(text)

    text = text.upper()

    return text


def protect_special_content(text: str, protected_spans: List) -> str:
    """保护URL和电子邮件"""
    for pattern in [r'https?://\S+', r'\b[\w.-]+@[\w.-]+\.\w+\b']:
        for match in re.finditer(pattern, text):
            protected_spans.append({
                'start': match.start(),
                'end': match.end(),
                'original': match.group()
            })
            text = (
                text[:match.start()]
                + f" 𝙋𝙍𝙊𝙏𝙀𝘾𝙏𝙀𝘿_{len(protected_spans)-1} "
                + text[match.end():]
            )
    return text


def restore_protected_content(text: str, protected_spans: List) -> str:
    """恢复被保护的内容"""
    for i, span in enumerate(protected_spans):
        text = text.replace(f"𝙋𝙍𝙊𝙏𝙀𝘾𝙏𝙀𝘿_{i}", span['original'])
    return text


def remove_accents(text: str) -> str:
    """移除重音符号（é → e）"""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')


def reduce_repeated_characters(text: str) -> str:
    """重复字母完全归约"""
    return re.sub(r'([a-zA-Z])\1+', r'\1', text)


def expand_contractions(text: str) -> str:
    """菲律宾语缩写展开（优先级从高到低）"""
    CONTRACTIONS = {
        # 整体替换优先
        r"'yung\b": "ang",
        r"'yng\b": "ang",
        r"'ung\b": "ang",
        r"d'yan\b": "diyan",
        r"n'ung\b": "ng",

        # 通用规则
        r"'y\b": "ang",
        r"'t\b": "at",
        r"'n\b": "ng",
        r"'di\b": "hindi",
        r"'pag\b": "kapag",
    }

    for pattern, replacement in CONTRACTIONS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def standardize_spelling(text: str) -> str:
    """标准化拼写（含大小写感知）"""
    SPELLING_VARIANTS = {
        'azucar': 'asukal',
        'kompyuter': 'komputer',
        'pamilya': 'pamilya',
        'nang': 'ng',
        'nang ': 'ng ',
    }

    words = text.split()
    normalized_words = []

    for word in words:
        original_word = word
        word_lower = remove_accents(word.lower())

        # 检查变体（忽略标点）
        word_stem = re.sub(r'[^\w]', '', word_lower)
        if word_stem in SPELLING_VARIANTS:
            normalized_word = adjust_case(word, SPELLING_VARIANTS[word_stem])
            punctuation = re.sub(r'[\w]', '', original_word)
            normalized_words.append(normalized_word + punctuation)
        else:
            normalized_words.append(word)

    return ' '.join(normalized_words)


def adjust_case(original: str, replacement: str) -> str:
    """智能大小写转换"""
    if original.isupper():
        return replacement.upper()
    elif original.istitle():
        return replacement.capitalize()
    return replacement.lower()


def clean_text(text: str) -> str:
    """最终清理"""
    text = re.sub(r'([.,!?])\1+', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_normalizer(language_code: str):
    if language_code.upper() in ('FIL', 'PHL'):
        return normalize
    raise ValueError(f"Unsupported language: {language_code}")
