# text_norm

本目录用于存放各语言的text_norm脚本。

**仅供内部测试使用，未经允许请勿在个人项目或论文中使用**

## 调用方法

```python
from scripts import get_normalizer

normalize = get_normalizer("ARE")  
text = normalize("示例文本")

```

## 命名规则

- **文件名必须使用三字母全大写代码（如 ARE、JPN、KOR）**

- 每个文件对应一种语言的文本规范化逻辑

- 示例：IRQ.py

### 通用规则
- `ALL.py` 会在任何国家/地区的 text_norm 之前执行，可在其中编写对所有语言都适用的规则。
- `ALL.py` 当前会移除统一的噪声/事件标签（如 `[UNK]`、`[breath]` 等）、删掉以 `#` 标记的填充词（示例：`#呃`、`#hmm`）、去掉剩余标点符号，最后压缩空白。
- `ALL.py` 的 `normalize()` 签名与其它语言脚本一致，返回的文本会继续传递给特定语言的 `normalize()`。

## 编写要求

每个语言文件必须实现以下函数：

```python
def normalize(text: str) -> str:
    """
    输入：原始文本
    输出：text_norm 后的文本
    """
```


