# 引用模式识别参考

## 支持的引用格式

### 1. 数字编号 (numeric)

```
[1]         → 单篇引用
[1,2]       → 多篇引用（逗号分隔）
[1-3]       → 连续引用（范围）
[1,2,5-7]   → 混合引用
[1, 2]      → 带空格
[1–3]       → en-dash
[1—3]       → em-dash
```

正则: `\[(?P<nums>\d+(?:\s*[-,]\s*\d+)*)\]`

### 2. 作者-年份 (author_year_paren)

```
(Smith et al., 2020)
(Zhang and Li, 2019)
(Wang, 2021)
(Smith et al., 2020a)
(Müller, 2018)
(O'Brien, 2022)
```

正则: `\((?P<auth>[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+(?:\s+(?:et\s+al\.|and\s+[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+))?),\s*(?P<year>\d{4}[a-z]?)\)`

### 3. 内联作者-年份 (inline_author_year)

```
Smith et al. (2020) found that...
Zhang and Li (2019) demonstrated...
According to Wang (2021)...
```

正则: `(?P<auth>[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+(?:\s+(?:et\s+al\.|and\s+[A-Z][a-zA-Záéíóúàèìòùäëïöüñç\-']+))?)\s+\((?P<year>\d{4}[a-z]?)\)`

### 4. 上标 (superscript)

```
text¹²³       → 多个上标数字
text¹,²       → 上标加逗号
text¹⁻³       → 上标范围（罕见）
```

正则: `[\u00B9\u00B2\u00B3\u2070\u2071\u2074\u2075\u2076\u2077\u2078\u2079]+`

## 边界情况

### 引用嵌套在括号中
```
(see [1] for review)
(see Smith et al., 2020)
```
处理：提取内层引用标记，忽略外层括号。

### 多个引用在同一句
```
Recent studies [1,2,3] have shown that Fe₃GeTe₂ exhibits...
```
处理：将 `[1,2,3]` 作为一个引用组，但在 Zotero 查询时拆分为三篇。

### 引用在句末
```
...as demonstrated by previous work. [1]
...as demonstrated by previous work [1].
```
处理：位置（句号前/后）不影响提取，但报告中应标注引用位置。

### 混合引用风格
```
Smith et al. [1] found that... while Zhang (2020) reported...
```
处理：分别提取数字引用和作者-年份引用。

## 数字引用到文献的映射

数字编号引用需要从论文的参考文献列表中解析对应关系。

### 自动解析策略

1. 在 liteparse 输出的 JSON 中查找包含 "References" / "参考文献" / "Bibliography" 的标题
2. 提取其后的文本，按编号模式 `[1]` / `1.` / `[1]` 分割
3. 对每条文献提取第一作者姓氏和年份
4. 建立编号 → 作者年份映射
5. 使用映射生成 Zotero 搜索查询

### 手动回退

如果自动解析失败，提示用户：
```
无法自动解析参考文献列表，请提供编号 [X] 对应的文献信息：
- 格式: "[1]: Smith, J. et al. Nature 2020, 580, 123-130"
```
