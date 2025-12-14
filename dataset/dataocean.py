# -*- coding: utf-8 -*-
"""
DataOcean 数据集专用文本规范化规则

声学事件标签说明（来自 DataOcean 官方规范）：
[breath]        呼吸声
[chocking]      哽咽
[humph]         哼声
[sigh]          叹气
[laugh]         笑声
[cough]         咳嗽
[hissing]       嘶声
[Throat clear]  清嗓子

填充词说明：
- 为表示说话者犹豫或维持话语权而使用的“词语”
- 每种语言有各自的填充词
- 每个填充词前使用井号（#）标记，如：
  #呃  #额  #嗯  #erm

说明：
- 本文件 **只处理 DataOcean 特有的声学标签与填充词**
- 不做标点删除、不压缩空格
- 最终清理由 main.py 统一完成
"""

import regex as re


# DataOcean 中的声学事件标签
DATAOCEAN_EVENT_PATTERN = re.compile(
    r"""
    \[breath\] |
    \[chocking\] |
    \[humph\] |
    \[sigh\] |
    \[laugh\] |
    \[cough\] |
    \[hissing\] |
    \[throat\s*clear\]
    """,
    flags=re.IGNORECASE | re.VERBOSE,
)

# DataOcean 填充词：以 # 开头的连续非空白字符
FILLER_MARK_PATTERN = re.compile(r"#\S+")


def normalize(text: str) -> str:
    """
    DataOcean 文本规范化入口函数

    参数：
        text (str): 原始转写文本

    返回：
        str: 删除声学事件标签与填充词后的文本
    """
    # 删除声学事件标签（如 [breath]、[cough] 等）
    text = DATAOCEAN_EVENT_PATTERN.sub(" ", text)

    # 删除以 # 标记的填充词（如 #呃、#嗯、#erm）
    text = FILLER_MARK_PATTERN.sub(" ", text)

    return text
