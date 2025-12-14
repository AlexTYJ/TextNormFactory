# -*- coding: utf-8 -*-
"""
text_norm 主入口文件

职责说明：
1. 调度 dataset 与 language 的 normalize 函数
2. 在 **所有 dataset / language 处理完成之后**
   执行统一的最终清理：
   - 删除所有标点和符号字符
   - 压缩连续空白

设计原则：
- dataset / language 可以依赖原始符号信息
- 标点与空格清理 **只能在最后一步**
"""

from importlib import import_module
from typing import Callable
import regex as re


# =============================
# 最终统一清理（最后一步）
# =============================

# Unicode 感知的标点 + 符号正则
PUNCT_PATTERN = re.compile(r"[\p{P}\p{S}]")


def final_clean(text: str) -> str:
    """
    最终清理函数（必须最后执行）

    操作：
    1. 删除所有标点和符号字符
    2. 去除首尾空白
    3. 将连续空白压缩为单个空格
    """
    text = PUNCT_PATTERN.sub(" ", text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


# =============================
# 动态加载 normalize 函数
# =============================

def _load_normalizer(module_path: str) -> Callable[[str], str]:
    """
    动态加载指定模块中的 normalize 函数

    参数：
        module_path (str): 模块路径，如 text_norm.dataset.magicdata

    返回：
        Callable: normalize(text: str) -> str
    """
    module = import_module(module_path)
    return module.normalize


# =============================
# 对外统一接口
# =============================

def get_normalizer(
    language: str,
    dataset: str | None = None,
) -> Callable[[str], str]:
    """
    获取文本规范化函数

    执行顺序（严格）：
        1. dataset.normalize（可选）
        2. language.normalize
        3. final_clean（标点删除 + 空格压缩）

    参数：
        language (str): 三字母语言代码，如 "ARE"、"IRQ"
        dataset (str | None): 数据集名称，如 "magicdata"、"dataocean"

    返回：
        Callable[[str], str]: 可直接调用的 normalize 函数
    """

    # 语言代码统一转为大写
    language = language.upper()

    # 加载语言规范化函数
    language_normalize = _load_normalizer(
        f"text_norm.language.{language}"
    )

    # 如果指定了数据集，则加载对应的 dataset 规范化函数
    dataset_normalize = None
    if dataset is not None:
        dataset_normalize = _load_normalizer(
            f"text_norm.dataset.{dataset.lower()}"
        )

    def normalize(text: str) -> str:
        """
        实际执行的文本规范化函数
        """
        # 先执行数据集规范化（如果有）
        if dataset_normalize is not None:
            text = dataset_normalize(text)

        # 再执行语言规范化
        text = language_normalize(text)

        # 最后执行统一清理（标点 + 空格）
        text = final_clean(text)

        return text

    return normalize
