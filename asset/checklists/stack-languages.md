# stack-languages — 评审清单

- [ ] blocking | 已指明实现语言与运行时版本（.NET TFM／MSVC 工具集／Rust crate） | dotnet_probe · sdk_probe
- [ ] blocking | PowerShell 判据标明宿主（5.1 `powershell.exe` 或 7 `pwsh.exe`） | 迁移文档
- [ ] blocking | 跨 shell 管道显式指定编码，未依赖默认（中文乱码可复现即缺陷） | [本地]
- [ ] blocking | DLL 加载路径经实测，安全搜索模式与旁加载风险已评估 | DLL 搜索顺序文档
- [ ] major | Windows 专有 API 有 TFM／`[SupportedOSPlatform]` 门控 | .NET 文档
- [ ] major | VC++ 运行时依赖策略明确（`vc_redist` 或自包含） | vc_redist 文档
- [ ] major | WPF／WinForms／WinUI 的选择给出可判据（UI 复杂度、无障碍、打包） | 官方文档
- [ ] major | WSL 互操作只作工具链，未把 Linux 路径当 Windows 应用运行时 | WSL 文档
- [ ] advisory | 语言级判据（所有权／UB／借用）转 `cpp-expert` 而非本技能自裁 | dependence
- [ ] advisory | 构建脚本无平台硬编码路径（`C:\Program Files` 假设须实测） | code-guidelines

## 不可再拓扑声明

「Rust windows-rs 投影」与「C++/WinRT 投影」共享同一取证手段（头文件／crate 版本实测），
不独立成叶。

## 相关

[细则](../knowledge/stack-languages.md) · [知识树](../../references/知识树/知识树.md)
