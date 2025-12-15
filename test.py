# -*- coding: utf-8 -*-
"""
TextNormFactory 多语种 sanity test

目的：
- 覆盖当前 language/ 目录中的所有主要语种
- 每个语种给一条「短但有信息量」的测试句
- 包含：
  - 标点
  - 数字 / 数字词
  - 噪声标注
- 直接打印 text norm 前 / 后，人工检查
"""

from main import get_normalizer


def run_case(lang: str, dataset: str | None, text: str):
    print("=" * 90)
    print(f"Language: {lang} | Dataset: {dataset}")
    print("Before:")
    print(text)

    normalize = get_normalizer(language=lang, dataset=dataset)
    out = normalize(text)

    print("After:")
    print(out)
    print()


def main():
    # ============================================================
    # Arabic 系（仅 sanity，不验证方言细节）
    # ============================================================
    run_case(
        "ARE",
        "magicdata",
        "[LAUGHTER] أنااا ٢٠٢٤ #اه + hello",
    )

    run_case(
        "EGY",
        "magicdata",
        "إزيك يا جماعة ده ١٢٣؟!",
    )

    run_case(
        "IRQ",
        "dataocean",
        "[breath] أنا خوش ٢٠٢٢",
    )

    # ============================================================
    # 中文 / 东亚
    # ============================================================
    run_case(
        "CHN",
        "magicdata",
        "今天 #呃 天气不错！！！123",
    )

    run_case(
        "JPN",
        "magicdata",
        "（テスト）今日は ５ 回目！！！",
    )

    run_case(
        "KOR",
        None,
        "[테스트] 오늘은 삼 번 문제",
    )

    # ============================================================
    # 欧洲语言
    # ============================================================
    run_case(
        "DEU",
        "magicdata",
        "(Kommentar) Das ist 42!!!",
    )

    run_case(
        "ITA",
        "magicdata",
        "(nota) Questo costa １２３ euro!!!",
    )

    # ============================================================
    # 东南亚
    # ============================================================
    run_case(
        "IDN",
        None,
        "[noise] Pak mau pergi ga ke kantor １２３?",
    )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 泰语（THA）
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    run_case(
        "THA",
        "dataocean",
        "[laugh] วันนี้หนูตื่นตอน 7 โมง #อ่า",
    )

    # ============================================================
    # 英语 / 其它
    # ============================================================
    run_case(
        "USA",
        "magicdata",
        "<noise> I paid 123 dollars!!!",
    )

    run_case(
        "PHL",
        "magicdata",
        "Email test@test.com!!! 2024",
    )


if __name__ == "__main__":
    main()
