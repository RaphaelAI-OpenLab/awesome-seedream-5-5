# 投稿与维护

提交一个案例时，请完成以下四项：

1. 提供作者原帖或原始页面，标明作者与发布日期。
2. 提供能直接证明 **Seedream 5.5** 版本的来源文字或截图，不混入 5.0、5.0 Pro、5.5 Pro 等版本。
3. 区分实际原始提示词、展示说明和自行编写的练习配方。拿到公开的完整原始提示词后，须将全文保存到 `prompt.text`，保留原文语言、标点与换行，并在中英文目录 README 和案例详情页的图片下方直接展示为可复制的 `text` 代码块；来源链接用于归因，不能代替提示词正文。
4. 提供原媒体地址与权利说明；完整原始文件的打包归档需记录明确许可。

## 数据位置

| 文件 | 用途 |
| --- | --- |
| `content/cases.json` | 正式来源案例，每个工作流计一个案例 |
| `content/categories.json` | 双语分类名称 |
| `content/social.json` | 社媒来源、版本核对和重复关系 |
| `content/recipes.json` | 仓库原创、尚未执行的练习配方 |
| `external-references/cases.json` | 独立外站待重做案例，包含原始提示词与逐轮编辑指令 |

修改后运行：

```bash
python3 scripts/build.py
python3 scripts/build_external_refs.py
python3 scripts/validate.py
python3 scripts/validate_external_refs.py
python3 scripts/build.py --check
python3 scripts/build_external_refs.py --check
```

不要手改生成的 README 和案例页。官方展示不等于独立复现；技术解码通过不等于人工视觉验收。

## 提示词状态

| 状态 | 含义 |
| --- | --- |
| `original` | 已收录作者公开的实际指令，保留原文，并在 README 与详情页直接展示全文 |
| `source-linked` | 完整原始提示词待核实，当前仅保存来源链接或展示说明；取得完整指令后补入正文并改为 `original` |
| `not-published` | 未找到完整输入，不补写为原始提示词 |

外站待重做库使用 `source-exact` 表示已收录来源公开的提示词原文，同样在目录 README 与详情页直接展示。多轮编辑的每一条已公开指令也须完整展示；操作摘要须明确标注，不能作为完整输入。修改生成器时保留这一展示方式，避免再次退化为只有来源链接。

## 权利问题

媒体与原始提示词不受仓库 MIT 许可覆盖。请通过问题表单指出案例 ID、原始来源和具体问题；维护者可以移除引用或更正归因。练习配方没有可宣称的生成效果，投稿者不得将练习配方与不对应的示例图配对为实测结果。
