# stack-languages — 技术栈与语言路径

## 判据范围

.NET 桌面栈（WPF / WinForms / WinUI 3）、原生 C++（Win32 + C++/WinRT）、C# 与 Rust
（`windows-rs`）三条实现路径，外加脚本层：PowerShell 5.1 vs 7、WSL 互操作、
DLL 加载顺序与 VC++ 运行时。

## 硬事实

- TFM 决定可用 API 集：`net8.0-windows` 才有 WPF/WinForms；Windows 专有 API 须门控。
- `powershell.exe`（5.1·.NET Framework·内置）与 `pwsh.exe`（7·.NET·独立安装）
  语法、默认编码、模块可用性不等价，判据必须指明宿主版本。
- 跨 shell 事故主因是编码：5.1 重定向偏 UTF-16LE／系统 ANSI，7 默认 UTF-8 无 BOM，
  管道传中文须显式 `-Encoding`。
- DLL 搜索顺序受安全搜索模式与 `SetDefaultDllDirectories` 影响；旁加载风险须实测。
- `vc_redist` 版本随 MSVC 主版本走；自包含发布可免除但增大体积。

## 取证命令

```powershell
python -B scripts/dotnet_probe.py
python -B scripts/sdk_probe.py
python -B scripts/os_probe.py --shell
```

## 边界

C++/C# 语言级判据转 `cpp-expert`；Python 转 `python-expert`；Qt 转 `qt-qtquick-expert`。

## 相关

[清单](../checklists/stack-languages.md) · [上一叶](platform-selection.md) ·
[降级策略](../../resistance/降级策略/降级策略.md)
