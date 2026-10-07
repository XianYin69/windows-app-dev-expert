# dependence（依赖声明）

本技能**不内嵌**其他技能正文；能力一律经声明获取。每行一条 `名称 | 类型 | 来源`，
类型为 skill|software|repo|doc。SMS 安装时对本目录条目与本体做同样检查与净化
（trust 标注·未审/隔离拒装·仓库下载须网络授权）。

```
cpp-expert             | skill    | local://cpp-expert
c-expert               | skill    | local://c-expert
python-expert          | skill    | local://python-expert
qt-qtquick-expert      | skill    | local://qt-qtquick-expert
interface-design-expert  | skill    | local://interface-design-expert
code-guidelines        | skill    | local://code-guidelines
file_ops               | skill    | local://skill_manage_system
git                    | software | system
python                 | software | system
powershell             | software | system
msvc                   | software | optional
windows-sdk            | software | optional
dotnet                 | software | optional
```

## 用途映射

| 依赖 | 承担能力 | 触发节点 |
|---|---|---|
| cpp-expert | C++ 语言级判据（所有权／UB／移动） | 专家判断（Win32 层之外） |
| c-expert | C 运行时、Win32 头文件与 ABI 判据 | 专家判断 |
| python-expert | 探针脚本的 Python 语言级判据 | 脚本构建 · 整体审查 |
| qt-qtquick-expert | Qt 在 Windows 的专项（平台插件／windeployqt／DPI） | 领域定位（转派） |
| interface-design-expert | 视觉／交互专项判断（本技能不自行裁视觉） | 领域定位（转派） |
| code-guidelines | 命名／注释／复杂度／评审通用准则 | 专家判断 · 整体审查 |
| file_ops | 联网检索取页、文件读写（API 与版本行为取证） | 浏览器学习 · 知识检索 |
| git | 功能分支→dev→main 工作流 | 初始化 · 收尾 |
| python | 运行 `scripts/` 探针 | 取证探查 · 整体审查 |
| powershell | 系统侧取证（Get-*／sc.exe／logman／signtool 包装） | 取证探查 |
| msvc | `cl`／`link`／`dumpbin` 实测编译与依赖 | 取证探查（缺即降级） |
| windows-sdk | 头文件／lib／`MakeAppx`／`signtool`／WPT 工具 | 取证探查（缺即降级） |
| dotnet | `dotnet --info`、WPF／WinForms 目标框架实测 | 取证探查（缺即降级） |

## 边界

- 跨技能只传「意图 + 参数」，由对方在其目录内执行；禁止直接 import 他技能模块。
- 依赖缺失：记 `process_chain interrupt` 并报告缺项，禁止伪造能力继续。
- 增删依赖须走 [update 审批流](../update/update.md) 并记 CHANGELOG；每条必附 `source_url`。
- 自检：`python -B scripts/knowledge_index.py --check-deps`

## 相关

- [deps.json](deps.json) · [薄技能依赖约束](../resistance/薄技能依赖约束/薄技能依赖约束.md)
