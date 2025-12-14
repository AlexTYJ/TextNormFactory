import re
import sys
import unicodedata

# --- 依赖库检查 ---
try:
    from underthesea import text_normalize as underthesea_normalize
except ImportError:
    print("错误: 未找到库 'underthesea'。请执行: pip install underthesea")
    sys.exit(1)

try:
    from num2words import num2words
except ImportError:
    print("错误: 未找到库 'num2words'。请执行: pip install num2words")
    sys.exit(1)


def _convert_numbers(text: str) -> str:
    """
    将文本中的数字转换为越南语读音。
    在转换结果前后添加空格，防止与周围字母粘连 (如 '4G' -> 'bốn g')。
    """
    return re.sub(r"\d+", lambda x: " " + num2words(int(x.group()), lang="vi") + " ", text)


def _remove_asr_tags(text: str) -> str:
    """
    移除 ASR 数据集中的非语言标记 (如 [laugh], <unk>, ++garbage++)。
    """
    # 移除标准括号标签 [], (), {}, <>
    text = re.sub(r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}|<[^>]*>", " ", text)
    # 移除特殊标记 (如 ++noise++)
    text = re.sub(r"\+\+[^\+]*\+\+", " ", text)
    return text


def _remove_punctuation(text: str) -> str:
    """
    旧版用于移除标点；现在标点已在 ALL.py 统一处理，
    这里只做额外字符清理（如将下划线视作空格）。
    """
    return text.replace("_", " ")


def normalize(text: str) -> str:
    """
    越南语 ASR 评测标准正则化入口函数。

    处理流程:
    1. Unicode NFC 归一化
    2. 移除 ASR 噪音标记
    3. Underthesea 文本标准化 (声调/拼写)
    4. 数字转文本
    5. 额外字符清理并转小写（标点由 ALL.py 统一删除）
    """
    if not text:
        return ""

    # Unicode NFC 归一化 (解决 NFD 分解字符问题)
    text = unicodedata.normalize("NFC", text)

    # 移除零宽字符
    text = re.sub(r"[\u200B\u200C\u200D\uFEFF]", " ", text)

    # 移除 ASR 噪音标记
    text = _remove_asr_tags(text)

    text = text.strip()

    # 文本标准化 (处理声调位置歧义，如 hòa/hoà)
    try:
        text = underthesea_normalize(text)
    except Exception:
        pass

    # 数字转文本
    text = _convert_numbers(text)

    # 移除标点并转小写
    text = _remove_punctuation(text)
    text = text.lower()

    # 合并多余空格
    text = re.sub(r"\s+", " ", text).strip()

    return text


if __name__ == "__main__":
    # --- 综合测试用例 ---

    test_cases = [
        # A 组：声调与拼写（新旧风格统一、特殊地名）
        ("A01", "Hoà bình, Thuỷ tinh, Qui Nhơn, Đắk Lắk", "hòa bình thủy tinh quy nhơn đắk lắk"),
        # B 组：编码与字符（NFD→NFC、特殊元音、全角字符）
        ("B01", "Tiê\u0301ng Viê\u0323t (NFD), Ưu đãi, ＡＢＣ", "tiếng việt ưu đãi abc"),
        # C 组：复杂数字与单位（小数、日期、IP、混合时间）
        (
            "C01",
            "1,000,000; 3.14; 20/11/2024; 192.168.1.1; $50; 8h30p",
            "một không không không không không không ba mười bốn hai mươi mười một hai nghìn không trăm hai mươi bốn một chín hai một sáu tám một một năm mươi tám h ba mươi p",
        ),
        # D 组：ASR 噪声与标签（嵌套/未闭合/特殊标记）
        ("D01", "Hello [laugh] (noise) <unk> {breath} ++garbage++ <silence>...", "hello"),
        # E 组：标点与特殊符号（邮箱、标签、连字符）
        ("E01", "user@email.com #hashtag Wi-fi_Zone A/B", "user email com hashtag wi fi zone a b"),
        # F 组：外来词（保留 F/J/Z/W 等非越南语字母）
        ("F01", "Vietnam Airlines, YouTube, Zalo, Jeans", "vietnam airlines youtube zalo jeans"),
        # G 组：边缘情况（混合格式、换行、零宽字符）
        ("G01", "123!!![laugh]\nLine2\tTab\u200bZero", "một trăm hai mươi ba line2 tab zero"),
        # H 组：误判防御（防止粘连并保留 +、C++ 等）
        ("H01", "4G LTE, F0, 1A, C++, K+, Vitamin 3B", "bốn g lte f không một a c + + k + vitamin ba b"),
        # I 组：科技与数学（化学式、平方、等式、版本号）
        ("I01", "H2O, CO2, m2, 1 + 1 = 2, v1.0.0", "h hai o co hai m hai một + một hai v một không không"),
        # J 组：混合语种（Code-switching）
        ("J01", "Sale 50%, Check mail, Log in", "sale năm mươi check mail log in"),
    ]

    print("--- 越南语 ASR 正则化测试结果 (垂直对比) ---")

    failures = 0
    for case_id, raw, expected in test_cases:
        output = normalize(raw)

        print(f"[{case_id}]")
        print(f"Raw : {raw}")
        print(f"Norm: {output}")

        # 简单验证: 输入含有效内容但输出为空则报警
        has_content = re.search(r"[a-zA-Z0-9]", raw)
        if has_content and not output.strip():
            print(f">>> 警告: 输入包含内容但输出为空!")
            failures += 1

        print("-" * 60)

    print(f"测试结束。共 {len(test_cases)} 个综合用例。")
    if failures > 0:
        print(f"发现 {failures} 个潜在问题。")
    else:
        print("所有用例检查通过。")
