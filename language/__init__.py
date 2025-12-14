# -*- coding: utf-8 -*-
"""
language 模块入口

职责：
- 根据三字母语言代码（如 ARE / IRQ / JPN）
  加载对应语言文件中的 normalize(text) 函数
- 不做 pipeline
- 不做全局规则
"""

import importlib
from typing import Callable


def _load_language_normalizer(lang_code: str) -> Callable[[str], str]:
    """
    动态加载 language/{LANG}.py 中的 normalize 函数

    参数：
        lang_code (str): 三字母语言代码（已转为大写）

    返回：
        Callable[[str], str]: normalize 函数
    """
    module_path = f"text_norm.language.{lang_code}"

    module = importlib.import_module(module_path)

    if not hasattr(module, "normalize"):
        raise AttributeError(
            f"{module_path}.py 必须定义 normalize(text: str) -> str"
        )

    return module.normalize


def get_language_normalizer(lang_code: str) -> Callable[[str], str]:
    """
    获取指定语言的 normalize 函数

    示例：
        normalize = get_language_normalizer("ARE")
        text = normalize("示例文本")
    """

    if not isinstance(lang_code, str):
        raise TypeError("lang_code 必须是字符串，例如 'ARE'")

    if len(lang_code) != 3:
        raise ValueError("lang_code 必须是 3 位语言代码，例如 'ARE'")

    # 强制使用大写模块名
    lang_code = lang_code.upper()

    return _load_language_normalizer(lang_code)
