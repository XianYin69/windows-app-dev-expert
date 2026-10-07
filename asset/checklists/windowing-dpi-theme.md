# windowing-dpi-theme — 评审清单

- [ ] blocking | DPI 感知等级在进程启动前设定（清单或 `SetProcessDpiAwarenessContext`） | DPI 文档
- [ ] blocking | 处理 `WM_DPICHANGED` 并采用建议矩形，缩放切换可复现无异常 | DPI 文档
- [ ] blocking | 跨显示器移动按目标屏 DPI 重算尺寸／字体，无像素常量硬编码 | dpi_probe
- [ ] blocking | 自定义标题栏处理 `WM_NCCALCSIZE`／`WM_GETMINMAXINFO`，最大化不遮任务栏 | 自定义框架文档
- [ ] major | 消息循环无阻塞（无同步等待、无启动期磁盘 I/O 在 UI 线程） | 消息循环文档
- [ ] major | 深色模式判定来源明确（系统资源读取或自绘），未写 HKCU 深色键 | uxtheme 文档
- [ ] major | 主题切换（浅↔深）后颜色与图标同步刷新，无残留白底 | [本地]
- [ ] major | 窗口尺寸遵循最小/最大约束与多屏工作区（含负坐标左屏） | dpi_probe
- [ ] advisory | 动画与过渡遵循系统「视觉效果」开关 | 平台文档
- [ ] advisory | 视觉层级与配色转 `interface-design-expert` | dependence

## 不可再拓扑声明

「DWM 合成」判据与 diagnostics-perf 的掉帧取证同源，不另立叶。

## 相关

[细则](../knowledge/windowing-dpi-theme.md) · [知识树](../../references/知识树/知识树.md)
