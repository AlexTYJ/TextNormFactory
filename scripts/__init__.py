import importlib
from typing import Callable

GLOBAL_NORMALIZER_CODE = "ALL"


def _load_normalizer(module_code: str) -> Callable[[str], str]:
    module = importlib.import_module(f"scripts.{module_code}")
    if not hasattr(module, "normalize"):
        raise AttributeError(f"{module_code}.py must contain a normalize(text) function")
    return module.normalize


def get_normalizer(lang_code: str):
    """
    Load the normalize() function from a language-specific module,
    identified by a three-letter uppercase language code.

    Example:
        normalize = get_normalizer("ARE")
        text = normalize("some text")
    """

    if not isinstance(lang_code, str):
        raise TypeError("lang_code must be a string, e.g. 'ARE'")

    if len(lang_code) != 3:
        raise ValueError("lang_code must be a 3-letter code, e.g. 'ARE'")

    # enforce uppercase module name
    lang_code = lang_code.upper()

    shared_normalizer = None
    try:
        shared_normalizer = _load_normalizer(GLOBAL_NORMALIZER_CODE)
    except ModuleNotFoundError:
        shared_normalizer = None

    lang_normalizer = _load_normalizer(lang_code)

    if shared_normalizer is None:
        return lang_normalizer

    def pipeline(text: str) -> str:
        return lang_normalizer(shared_normalizer(text))

    return pipeline
