# scripts（脚本库）

薄探针：只读取证、可独立运行、英文命名。脚本不限行数，但禁裸 `except`、
调试残留、> 100 字符长行与超长函数。全部脚本相对技能根真实存在。

## 清单（12 个探针 + 1 个共用模块）

| 脚本 | 作用 | 典型调用 |
|---|---|---|
| `classify_topic.py` | 关键词→叶映射（数据源知识树） | `--query "<问题>"` |
| `knowledge_index.py` | 叶索引／详情／清单原文／依赖校验 | `--check-deps` |
| `review_checklist.py` | 生成勾选模板并统计未通过项 | `--leaf <id>` |
| `check_links.py` | 悬空链接为 0 与 .md ≤ 50 行自检 | `--root .` |
| `os_probe.py` | OS 版本／架构／域／shell／目录／无障碍 | `--shell --paths --a11y --domain` |
| `sdk_probe.py` | Windows SDK 与 MSVC 工具集 | `--tools --runtime` |
| `dotnet_probe.py` | .NET SDK／运行时／桌面框架 | `--desktop` |
| `sign_probe.py` | Authenticode 签名与证书链 | `-Path app.exe --store` |
| `etw_probe.py` | ETW 会话与事件日志可读性 | `--sessions --log Application` |
| `dpi_probe.py` | 逐显示器 DPI／深浅色开关 | `--theme` |
| `service_probe.py` | 服务／计划任务／启动项状态 | `--services --tasks` |
| `msix_probe.py` | 包清单、框架依赖、包标识 | `--deps -PackageFamilyName` |
| `_common.py` | 共用模块（PowerShell 调用、参数、知识树读取） | 由探针 import |

## 约定

- 返回码：0 取证成功；2 用法错误；3 工具链缺失（须走降级策略）；4 数据缺失。
- 探针一律**只读**：不写注册表、不装服务、不创建 ETW 会话（副作用须用户授权）。
- PowerShell 走 `powershell.exe`（5.1，系统内置）；需 7 特性时由调用方显式指定。
- 输出压缩：探针打印关键行，禁止整段粘贴日志（见上下文压缩机制）。

## 相关

- [降级策略](../resistance/降级策略/降级策略.md) ·
  [取证探查节点](../branch/流程/取证探查/取证探查.md) · [SKILL.md](../SKILL.md)
