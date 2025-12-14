import re
import unicodedata

def normalize(text: str) -> str:
    """
    泰语 CER 评测使用的完整规范化流程：
    - Unicode NFC 规整（确保声调符号顺序正确）。
    - 删除括号内的噪声标注（[laugh]、(noise) 等）。
    - 移除零宽字符。
    - 仅删除符号字符 '#'（不删除其后文本）。
    - 转换英文数字为泰语数字。
    - 删除泰文范围外的字符（相当于去标点/空格）。
    - 最后再次 NFC，保证组合顺序稳定。
    """
    # 英文数字 → 泰文数字
    EN2TH_DIGITS = str.maketrans({
        "0": "๐",
        "1": "๑",
        "2": "๒",
        "3": "๓",
        "4": "๔",
        "5": "๕",
        "6": "๖",
        "7": "๗",
        "8": "๘",
        "9": "๙",
    })

    # 零宽字符
    ZERO_WIDTH_CHARS = r"\u200B\u200C\u200D\uFEFF"

    # 噪声标签：如 [laugh]、(noise)、{breath}
    BRACKET_PATTERN = r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}"

    # 1. Unicode NFC normalization (VERY IMPORTANT)
    text = unicodedata.normalize("NFC", text)

    # 2. Remove annotation inside [], (), {}
    text = re.sub(BRACKET_PATTERN, "", text)

    # 3. 删除 '#' 字符
    text = text.replace("#", "")

    # 4. 移除零宽字符
    text = re.sub(f"[{ZERO_WIDTH_CHARS}]", "", text)

    # 5. 英文数字 → 泰文数字
    text = text.translate(EN2TH_DIGITS)

    # 6. 仅保留泰文字符（含泰国数字），其余统统删除
    text = re.sub(r"[^\u0E00-\u0E7F]", "", text)

    # 7. 再次 NFC，保证组合字符顺序一致
    text = unicodedata.normalize("NFC", text)

    return text


if __name__ == "__main__":
    for item in [
        "ไม่ ไม่ [laugh] ไม่ หนูไม่ได้ตั้งใจ",
        "(เสียงหัวเราะ) ก็แบบว่า หนูตกใจมาก",
        r"พี่เค้าพูดว่า {breath} เดี๋ยวมาแป๊บนึงนะ",
        "พอดีอยู่ข้างพี่แอฟ # อ่า ต้องรีบไป",
        "วันนี้หนูตื่นตอน 7 โมง",
        "พี่คะ [laugh] หนูถึงบ้านแล้วค่าาา~ 555 😂😂",
        "โอเคค่ะ 100%",
        "เก๋"
    ]:
        print(f"{item}\n{normalize(item)}\n------")
