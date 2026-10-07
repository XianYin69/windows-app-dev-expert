# windowing-dpi-theme — 窗口·消息循环·DPI·深色模式

## 判据范围

窗口与消息循环（`WndProc`/`GetMessage`/`DispatchMessage`）、DPI 感知等级与多显示器、
深色模式（应用与系统资源）、自定义标题栏与 DWM 合成边界。

## 硬事实

- DPI 感知等级由清单／`SetProcessDpiAwarenessContext` 在**进程启动前**决定，
  运行中改不了；`Per-Monitor V2` 才拿到逐窗口 DPI（`GetDpiForWindow`）。
- 缩放变化经 `WM_DPICHANGED` 给出建议矩形；未处理即断言「高分屏正常」无效。
- 跨屏移动须按目标屏 DPI 重算尺寸与字体，像素常量（如 320px）须换算。
- 深色模式：Win32 走 `uxtheme` 的 `SetPreferredAppMode`（版本相关）或自绘资源；
  注册表 `AppsUseLightTheme` 属 HKCU 读取，不得当作可写配置项建议。
- 自定义标题栏须处理 `WM_NCCALCSIZE`／`WM_GETMINMAXINFO` 与工作区，
  否则最大化遮挡任务栏——判据须给可复现的窗口消息序列。

## 取证命令

```powershell
python -B scripts/dpi_probe.py           # 逐显示器 DPI／缩放／工作区
python -B scripts/os_probe.py            # 构建号决定可用 DPI API
```

## 边界

视觉与交互取舍转 `interface-design-expert`；Qt 窗口系统转 `qt-qtquick-expert`。

## 相关

[清单](../checklists/windowing-dpi-theme.md) · [上一叶](stack-languages.md) ·
[可访问性](accessibility-uia.md)
