# CHANGELOG
## 0.1.0 — 2026-10-07
- 初版：Windows 桌面／系统应用薄顾问技能，结构对齐 `cpp-expert` / `qt-qtquick-expert` /
  `interface-design-expert`；范围排除 Qt 与 Web 前端（分别转派）。
- 知识树九叶：platform-selection · stack-languages · windowing-dpi-theme · accessibility-uia ·
  storage-config · ipc-background · services-privileges · signing-packaging · diagnostics-perf
  （按「独立取证手段＋独立评审清单＋判据不互相蕴含」判定不可再拓扑）。
- `asset/knowledge_tree.json` 机读索引 + `asset/knowledge/`（九叶细则）+ `asset/checklists/`
  + `asset/templates/`（最小骨架：Win32 窗口／App Manifest／MSIX 清单）。
- `scripts/` 12 个薄脚本：classify_topic / knowledge_index / review_checklist / check_links /
  os_probe / sdk_probe / dotnet_probe / sign_probe / etw_probe / dpi_probe / service_probe /
  msix_probe（每个带 `.py` 扩展名且相对技能根真实存在）。
- `dependence/deps.json`：本地技能与微软官方仓库／文档条目逐条附 `source_url`
  （联网核验 2026-10-07，HEAD 全部 200）。
- `resistance/`：git 工作流、平台假设、企业环境、注册表与服务安全、浏览器学习、薄技能依赖、
  审查约束、降级策略、沙盒、五大机制。
- `planned_tasks/`：初始化即建目录（README.md + template.json），当前无到期任务。
- MIT `LICENSE`、`.gitignore`（含 `tmp/`、IDE 与构建产物）、独立 git 仓（feature → dev → main
  本地提交，不推远端）。
- 违规后果：臆造 URL → 误导选型决策；跳过探针实测 → 结论不可复现；擅改 HKLM／服务 →
  目标机不可逆损伤；直写 main → 无法按步回滚。
