# asset（技能包资产）

本目录是**机读 + 人读**的资产层，SMS 安装时随本体一起校验与净化。

## 内容

- [`knowledge_tree.json`](knowledge_tree.json)：九叶机读索引（id/priority/title/keywords/
  probes/cites/knowledge/checklist 路径），`classify_topic.py` 与 `knowledge_index.py` 的唯一数据源。
- [`knowledge/`](knowledge/)：九叶细则与判据（每叶一份，含取证命令与边界声明）。
- [`checklists/`](checklists/)：九叶评审清单（`- [ ] 级别 | 判据 | 出处` 格式）。
- [`templates/`](templates/)：可复制的最小骨架（Win32 窗口与消息循环、应用清单、MSIX 清单）。

## 约定

- 叶 id 与 `knowledge/`、`checklists/` 文件名严格一致（`<叶>.md`）。
- 判据出处只写文档名/页面名，不写未确证的 URL；未确证条目在清单里标 `[本地]`。
- 新增叶须同步 `knowledge_tree.json`、`references/知识树/知识树.md` 与 `SKILL.md` 知识树段。
- 范围外内容（Qt、Web 前端、数据库、并发架构）不落本目录，走 `dependence/` 转派。

## 相关

- [知识树索引](../references/知识树/知识树.md) · [参考书目](../references/参考书目/参考书目.md)
- [scripts](../scripts/scripts.md)
