import regex as re


def arabic_text_normalize(text):
    """
    将其他阿拉伯方言的变体，统一为阿尔及利亚方言变体
    """
    stop_words = {
        # ==== 犹豫 / 思考 ====
        'ااا', 'آآآ', 'اممم', 'إممم', 'ممم', 'أمم', 'هممم',
        'إيه', 'إي', 'إييه',

        # ==== 感叹 / 反应 ====
        'آ', 'آه', 'آها', 'أوه', 'أوو', 'إيوا', 'إيوة',
        'هيه', 'ههه', 'هاه',

        # ==== 转折 / 承接 ====
        'طيب', 'يعني', 'بس', 'أها', 'المهم', 'خلاص', 'تمام',
        'بصراحة', 'شوف', 'والله',

        # ==== 呼语 / 引起注意 ====
        'يا', 'وي', 'وَيْ', 'وييي', 'ألو', 'لك',

        # ==== 方言填充词 ====
        # 黎凡特
        'شو', 'هيك',
        # 马格里布
        'هاك', 'باه', 'هاو', 'ياودي', 'هاديك',
        # 海湾方言
        'زين', 'عد', 'هاه',

        # ==== 拖时间 / 强调 ====
        'كذا', 'كذا يعني', 'زي', 'مثل',

        # ==== 让人安静 / 其他声音 ====
        'ششش', 'هههه', 'مممم'
    }
    

    # 备用的停用词集合（按需求扩展）
    #     'اا', 'ااا', 'ام', 'أمم', 'إممم', 'امم', 'ممم', 'آ', 'آه', 'آها', 'اه', 'إيه', 'إي',
    #     'طيب', 'يا', 'أوه', 'وَيْ', 'ششش', 'هيه', 'ه', 'او', 'يعني', 'حاجة', 'بص', 'شوف',
    #     'حسنا', 'اوكي', 'ماشي', 'ايوا', 'ها', 'تمام', 'خلاص', 'كويس'
    # }

    # 归一化拖长的声音与笑声
    long_aaa_re = re.compile(r'ا{3,}')         # 连续的 ا
    long_hhh_re = re.compile(r'ه{3,}')         # 连续的 ه（哈哈声）
    long_mmm_re = re.compile(r'م{3,}')         # 连续的 م（嗯声）
    long_alif_re = re.compile(r'آ{2,}')        # 连续的 آ

    if isinstance(text, str):
        text = text.split()
    else:
        assert isinstance(text, list)

    filtered = []
    for w in text:
        # 之前会在此处去除标点，现由 ALL.py 统一处理

        w = long_aaa_re.sub('', w)
        w = long_hhh_re.sub('', w)
        w = long_mmm_re.sub('', w)
        w = long_alif_re.sub('', w)

        if w == '' or w in stop_words:
            continue
        filtered.append(w)
    return ' '.join(filtered)


def normalize(text: str) -> str:
    """
    阿尔及利亚阿拉伯语文本标准化步骤（参考公开榜单）：
    1. 移除重音符号。
    2. 统一 Hamza/Madda 及波斯字母扩展。
    3. 只保留阿拉伯字母和数字，并规整空格。
    4. 将东阿数字、全角数字映射为西阿数字。
    """
    # 移除阿拉伯语重音符号（Fatha、Damma 等）
    diacritics = r"[\u064B-\u0652]"
    text = re.sub(diacritics, "", text)
    
    # 仅保留阿拉伯字母与数字
    text = re.sub(r"[^\p{Arabic}0-9]+", " ", text).strip()

    # 规范化多余空格
    text = re.sub(r"\s\s+", " ", text)

    """
    Hamza、Madda 与波斯字母的归一化会影响语义，
    建议仅在评测阶段启用，如需用于训练请自行评估。
    """
    text = re.sub("پ", "ب", text)
    text = re.sub("ڤ", "ف", text)
    text = re.sub(r"[آ]", "ا", text)
    text = re.sub(r"[أإ]", "ا", text)
    text = re.sub(r"[ؤ]", "و", text)
    text = re.sub(r"[ئ]", "ي", text)
    text = re.sub(r"[ء]", "", text)

    text = re.sub(r'\u0640', '', text)      # 去掉拉长线 tatweel

    # 将全角数字转为半角
    fullwidth_digits = str.maketrans(
        "０１２３４５６７８９",
        "0123456789"
    )
    text = text.translate(fullwidth_digits)

    eastern_arabic_digits = str.maketrans(
        "٠١٢٣٤٥٦٧٨٩",
        "0123456789"
    )
    text = text.translate(eastern_arabic_digits)

    text = re.sub(r'\u0640\u0651\u0653\u0654\u0655\u061C\u066B\u066C\u0671', '', text)  
    """
    \u0640: tatweel（拉长符）
    \u0651: Shadda（辅音强调）
    \u0653: Maddah Above（长元音组合）
    \u0654: Hamza Above
    \u061C: 文字方向控制符
    \u0655: Hamza Below
    \u066B: 阿拉伯小数点
    \u066C: 阿拉伯千位分隔符
    \u0671: Alif Wasla（宗教文本常见）
    """
    # 如需进一步兼容 U+069C，可手动替换为 U+0634
    # 可启用：return text.replace('ڜ', 'ش')

    return text


if __name__ == "__main__":
    examples = [
        "سلام، كيفاش داير؟ بغيت نخرج دابا... شنو غادي نديرو؟",
        "والله ما بغيتش نجي، علاش جيتي متأخر؟ ٣ ساعات وانا نستناك!",
        "Inchallah ghada nshri l-karhab 7mra, 2 litres dyal lmazot wakha?",
        "كما يمتو على عضان [laugh] أنعم إيه.",
        " [cough] ملكنا يا الحنين قهرونا المسؤولين.",
        "ان خوها اللي بغا يخرجها من الدار [breath] غادي نسمعو القصة ديالها.",
        "هادي ٢٠ درهم، بغيت جوج كيلو ديال الطماطم، ماشي غالية بزاف؟",
        "لا والله، صافي كملنا، سمحلي ولكن ما بغيتش هادشي"
    ]
    
    print("原始 → 标准化后\n")
    for ex in examples:
        print(f"{ex}")
        print(f"{normalize(ex)}\n")
