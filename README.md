# TextNormFactory

> **仅供内部测试，未经许可不得对外使用!!!!!!!!!!!!!**

TextNormFactory 面向多语种 ASR/WER 评测，执行顺序固定为：

```
原始文本 → dataset 模块 → language 模块 → main.final_clean()
```

## 目录结构

```text
TextNormFactory/
├── main.py          # 统一入口与执行顺序控制
├── dataset/         # 各数据集的标注/噪声规则
│   ├── magicdata.py
│   └── dataocean.py
└── language/        # 各语言的文本规范化规则
    ├── ARE.py
    ├── IRQ.py
    └── JPN.py
```

## 使用方法

1. **导入接口**（在仓库根目录运行脚本时最直接）
   ```python
   from main import get_normalizer
   ```
2. **获取 `normalize` 函数**
   ```python
   normalize = get_normalizer(
       language="ARE",      # 三字母语言代码（必须大写）
       dataset="magicdata", # 数据集名称（可选，小写）
   )
   ```
3. **执行文本规范化**
   ```python
   text = normalize("原始转写文本")
   ```

### 参数说明

- **language**：三字母大写语言代码（如 ARE、IRQ、JPN），对应 `language/{LANG}.py`。
- **dataset（可选）**：小写字符串（如 magicdata、dataocean），对应 `dataset/{dataset}.py`。若缺省则跳过数据集级规范化。

### 规范化执行顺序

1. 原始文本  
2. `dataset.normalize()`（若指定 dataset）  
3. `language.normalize()`  
4. `final_clean()`（删除标点 + 压缩空格）

### 各阶段职责

- **dataset 层**：处理数据集特有噪声标签、声学事件、填充词等；可能依赖原始符号（如 `[]`、`+`、`#`）；不删除标点、不压缩空格。
- **language 层**：处理语言相关规则（书写系统、语言习惯等）；不关心数据集标注格式；不删除标点。
- **final_clean（最后一步）**：删除所有 Unicode 标点与符号字符，将连续空白压缩为单个空格，确保最终输出格式一致。

## 支持语言

| 代码 | 语言 / 方言 | 说明 |
| --- | --- | --- |
| ARE | 阿联酋阿拉伯语 | 去 Tashkeel，统一 Hamza/波斯字母，过滤长音犹豫，东阿数字转西阿数字 |
| CHN | 普通话（简体） | 去除标点后保留汉字，将阿拉伯数字转中文数字 |
| DEU | 德语 | NFKC，删除括号标注，数字转德语单词，最终大写 |
| DZA | 阿尔及利亚阿拉伯语 | 去重音，统一 Hamza/Madda/波斯字母，保留阿拉伯字母与数字 |
| EGY | 埃及阿拉伯语 | Alef/Hamza 标准化，数字转阿拉伯文形式，常见方言词归一 |
| IDN | 印尼语 | Unicode 规整，清理噪声/填充词，TSV 映射货币/度量/时区，缩写统一 |
| IRQ | 伊拉克阿拉伯语 | 去重音，统一 Hamza/Madda，东阿数字转西阿数字，Tatweel 与犹豫词删除 |
| ITA | 意大利语 | NFKC，删除括号注释，数字转意大利语单词，最终大写 |
| JPN | 日语 | NFKC，删除括号注释，数字转日语大写，保留假名与 CJK |
| KOR | 韩语 | NFKC，删除括号注释，数字转韩语读法，仅保留谚文与英文字母 |
| MAR | 摩洛哥阿拉伯语 | 去重音，统一波斯/方言变体，数字半角化，常见 Darija 词映射 |
| MYS | 马来语 | 清理不可见字符，保留拉丁字母/数字，缩写与拼写变体映射，货币/单位空格修复 |
| PHL | 菲律宾语 | 保护 URL/邮箱，去重音，重复字母收缩，缩写与拼写标准化，最终大写 |
| SAU | 沙特阿拉伯语 | 去重音，统一 Alef/Ya/Ta Marbuta，删除 Tatweel，规整空白 |
| THA | 泰语 | NFC，清理噪声标签和零宽字符，数字转泰文，仅保留泰文字母 |
| USA | 英语（美式） | 过滤特定噪声行，删除填充词/尖括号标签/标点单词，数字转英文单词后大写 |
| VNM | 越南语 | NFC，零宽字符处理，Underthesea 标准化，数字转读音，保留外来字符 |

## 数据集

| 数据集 | 模块 | 说明 |
| --- | --- | --- |
| MagicData | `dataset/magicdata.py` | 删除 MagicData 标签（如 `[LAUGHTER]`、`[PII]`、`+`） |
| DataOcean | `dataset/dataocean.py` | 删除 `[breath]` 等声学事件标签与 `#` 填充词 |

## 开发要求

1. 模块只暴露 `normalize(text: str) -> str`。
2. 语言文件使用三字母大写代码，数据集文件使用小写。
3. dataset 与 language 只处理本层逻辑，标点和空格留给 `final_clean()`。
4. 注释使用中文，解释关键规则或正则。
5. 复杂逻辑建议在 `__main__` 中附自检用例。
