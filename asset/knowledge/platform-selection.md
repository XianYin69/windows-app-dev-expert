# platform-selection — 平台与形态选型

## 判据范围

Win32 / COM / WinRT 三层 API 模型的关系，以及桌面应用形态选型：
传统 Win32 桌面、UWP（已冻结）、WinUI 3 + Windows App SDK、打包（MSIX／包标识）与非打包。

## 硬事实（须引官方文档）

- UWP 的 `Windows.UI.Xaml` 不再演进；WinUI 3 走 `Microsoft.UI.Xaml` + Windows App SDK。
- Windows App SDK 有「框架包（依赖安装）」与「自包含（随应用发布）」两种部署模式，
  二者对打包要求、更新方式、企业分发影响不同，断言前须指明用的哪一种。
- 包标识（package identity）决定 `Windows.Storage.ApplicationData` 是否可用；
  非打包进程调用需包标识的 API 会失败——须先实测 `msix_probe`。
- COM 与 WinRT 的失败传播都是 `HRESULT`；C++/WinRT 抛异常只是投影，跨边界仍要查 `hr`。

## 取证命令

```powershell
python -B scripts/os_probe.py            # 版本／BuildLab／SKU／虚拟化与沙盒
python -B scripts/msix_probe.py          # 包清单、依赖、当前进程是否有包标识
python -B scripts/sdk_probe.py           # Windows SDK 与 MSVC 工具集是否齐备
```

## 边界

- Qt 桌面选型转 `qt-qtquick-expert`；Web／混合前端转 `interface-design-expert`。
- 语言级判据（所有权、UB、移动语义）转 `cpp-expert` / `c-expert` / `python-expert`。
- 本叶只出「形态与依赖模式」判断，不替用户裁商业许可与团队偏好。

## 相关

- 清单 [checklists/platform-selection.md](../checklists/platform-selection.md)
- 下一叶 [stack-languages](stack-languages.md) · [降级策略](../../resistance/降级策略/降级策略.md)
