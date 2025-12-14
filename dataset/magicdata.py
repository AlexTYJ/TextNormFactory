# -*- coding: utf-8 -*-
"""
MagicData 数据集专用文本规范化规则

标签说明（来自 MagicData 官方规范）：
+            overlapping speech（重叠语音）
[*]          unintelligible words or sentences（无法听清的词或句子）
[LAUGHTER]   laughter（笑声）
[SONANT]     干扰性发声噪声，如咳嗽、喷嚏、清嗓等
[MUSIC]      音乐或哼唱
[SYSTEM]     录音或通信系统产生的非语音噪声
[ENS]        环境噪声，如敲击、摩擦、动物声等
[FILLER]     独立出现的简单应答，如 “yes”“um”
[PII]        个人身份信息（Personally Identifiable Information）

说明：
- 本文件 **只处理 MagicData 特有的标注标签**
- 不做标点删除、不压缩空格
- 最终标点和空格处理由 main.py 统一完成
"""

import regex as re


# MagicData 中出现的噪声 / 事件标签正则
MAGICDATA_PATTERN = re.compile(
    r"""
    \+ |
    \[\*\] |
    \[LAUGHTER\] |
    \[SONANT\] |
    \[MUSIC\] |
    \[SYSTEM\] |
    \[ENS\] |
    \[FILLER\] |
    \[PII\]
    """,
    flags=re.IGNORECASE | re.VERBOSE,
)


def normalize(text: str) -> str:
    """
    MagicData 文本规范化入口函数

    参数：
        text (str): 原始转写文本

    返回：
        str: 删除 MagicData 标注标签后的文本
    """
    # 将所有 MagicData 标签替换为空格，保留原始文本结构
    return MAGICDATA_PATTERN.sub(" ", text)
