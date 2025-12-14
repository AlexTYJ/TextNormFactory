# -*- coding: utf-8 -*-
"""
TextNormFactory 多语种 sanity test

目的：
- 覆盖当前 language/ 目录中已有的语种
- 每个语种给一条“代表性短句”
- 尽量包含：
  - 标点
  - 数字
  - 数据集特殊标记（如 [LAUGHTER]、[breath]、#填充词）
- 直接打印 text norm 前 / 后，人工检查效果
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
    # ===============================
    # Arabic 系
    # ===============================
    run_case(
        "ARE",
        "magicdata",
        " [LAUGHTER] أَنَااا #اه سعيدٌ ٢٠٢٤!!! + hello ",
    )

    run_case(
        "DZA",
        "magicdata",
        "رَاهْ #اه الجوّ مْلِيح ٢٠٢٣!!! [PII]",
    )

    run_case(
        "EGY",
        "magicdata",
        "إحنا #اه رايحين ١٢٣؟!! [LAUGHTER]",
    )

    run_case(
        "IRQ",
        "dataocean",
        "[breath] أَنـا #嗯 خوش ٢٠٢٢!!! [cough]",
    )

    run_case(
        "MAR",
        "magicdata",
        "واش #اه لاباس؟ 2024!!! [LAUGHTER]",
    )

    run_case(
        "SAU",
        "magicdata",
        "هــذا #اه جيدٌ ٢٠٢٥!!! +",
    )

    # ===============================
    # 中文 / 东亚
    # ===============================
    run_case(
        "CHN",
        "magicdata",
        "今天 #呃 天气不错!!! 123 [LAUGHTER]",
    )

    run_case(
        "JPN",
        "magicdata",
        "（テスト）#erm 今日は 5 回目!!! [LAUGHTER]",
    )

    run_case(
        "KOR",
        "magicdata",
        "(테스트) #um 오늘은 3번째!!! [LAUGHTER]",
    )

    run_case(
        "THA",
        "dataocean",
        "[breath] วันนี้ #อืม 12 ครั้ง!!!",
    )

    # ===============================
    # 欧洲语言
    # ===============================
    run_case(
        "DEU",
        "magicdata",
        "(Kommentar) #äh Das ist 42!!!",
    )

    run_case(
        "ITA",
        "magicdata",
        "(nota) #eh Questo è 15!!!",
    )

    # ===============================
    # 东南亚
    # ===============================
    run_case(
        "IDN",
        "dataocean",
        "[breath] #eh Harga 20kg = 50rb!!!",
    )

    run_case(
        "MYS",
        "magicdata",
        "Ini #eh harga RM20.50!!!",
    )

    run_case(
        "VNM",
        "dataocean",
        "Hôm nay #ờ 12 lần!!!",
    )

    # ===============================
    # 英语 / 菲律宾
    # ===============================
    run_case(
        "USA",
        "magicdata",
        "<noise> #um I paid 123 dollars!!!",
    )

    run_case(
        "PHL",
        "magicdata",
        "Email: test@test.com!!! #uh 2024",
    )


if __name__ == "__main__":
    main()
