import re
import unicodedata

def normalize(text: str) -> str:
    """
    Most complete Thai normalization for CER:
    - Unicode NFC normalization (critical for Thai tone/vowel combining order)
    - Remove bracketed content [laugh], (noise)
    - Remove zero-width characters
    - Remove only '#' symbol (not following content)
    - Remove punctuation
    - Convert English digits to Thai digits
    - Remove English/Chinese punctuations
    - Remove spaces (Thai doesn't use them for CER)
    - Keep only Thai characters + Thai digits
    - Final char-level spacing for CER
    """

    # Thai digits → ASCII digits (012345)
    EN2TH_DIGITS = str.maketrans({
        "๐": "0",
        "๑": "1",
        "๒": "2",
        "๓": "3",
        "๔": "4",
        "๕": "5",
        "๖": "6",
        "๗": "7",
        "๘": "8",
        "๙": "9",
    })

    ZERO_WIDTH_CHARS = r"\u200B\u200C\u200D\uFEFF"
    BRACKET_PATTERN = r"\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\}"

    # 1. Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)

    # 2. Remove annotation
    text = re.sub(BRACKET_PATTERN, "", text)

    # 3. Remove '#' only
    text = text.replace("#", "")

    # 4. Remove zero-width chars
    text = re.sub(f"[{ZERO_WIDTH_CHARS}]", "", text)

    # 5. Thai digits → ASCII digits
    text = text.translate(EN2TH_DIGITS)

    # 6. Keep only Thai chars + digits
    text = re.sub(r"[^\u0E00-\u0E7F0-9]", "", text)

    # 7. Final NFC (safety)
    text = unicodedata.normalize("NFC", text)

    # ======== CER 用：字符级空格化（唯一新增）========
    text = " ".join([ch for ch in text if ch.strip() != ""])

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
