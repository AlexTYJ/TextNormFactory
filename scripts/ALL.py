"""
通用的文本规范化步骤，在调用每个国家/地区的 normalize 之前会先执行这里的逻辑。
可以在这里编写所有语言都需要共享的正则或替换规则。
"""

import regex as re

NOISE_TAG_PATTERN = re.compile(
    # 标签说明：
    # [*] 无法听清的句子
    # [UNK] 无法听清的词
    # [+] 重叠语音
    # [LAUGHTER] 笑声
    # [SONANT] 咳嗽/喷嚏/清嗓等声带噪声
    # [MUSIC] 音乐或哼唱
    # [SYSTEM] 录音/通信系统噪声
    # [ENS] 其它环境噪声
    # [NPS] 非主说话人
    # [PII] 个人身份信息
    # 额外的声学标注：
    # [breath], [chocking], [humph], [sigh], [laugh], [cough], [hissing], [Throat clear]
    r"\[(?:\*|UNK|\+|LAUGHTER|SONANT|MUSIC|SYSTEM|ENS|NPS|PII|breath|chocking|humph|sigh|laugh|cough|hissing|throat\s*clear)\]",
    flags=re.IGNORECASE,
)

# 语料中以“#词”的形式标记填充词，这里统一删除。
FILLER_MARK_PATTERN = re.compile(r"#\S+")

# 在去掉特殊标签后，再清理剩余的标点与符号字符。
PUNCT_PATTERN = re.compile(r"[\p{P}\p{S}]")


def normalize(text: str) -> str:
    """
    通用规范化流程：
        1. 移除标注噪声/系统事件的标签，如 [UNK]、[LAUGHTER]、[breath] 等。
        2. 移除以井号标记的填充词（如 #呃、#mmm）。
        3. 移除剩余的标点/符号字符。
        4. 去掉首尾空白并压缩连续空白为单个空格。
    可根据需要继续扩展此函数。
    """
    text = NOISE_TAG_PATTERN.sub(" ", text)
    text = FILLER_MARK_PATTERN.sub(" ", text)
    text = PUNCT_PATTERN.sub(" ", text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


if __name__ == "__main__":
    demo = " [LAUGHTER]! [breath], 呃 #呃  hello?!  [+] world [UNK] #hmm "
    print(normalize(demo))
