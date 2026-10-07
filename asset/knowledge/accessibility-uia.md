# accessibility-uia — 可访问性（UIA）

## 判据范围

UIA 树与属性（`Name`/`AutomationId`/`ControlType`）、控件模式（Invoke/Value/
SelectionItem 等）、键盘导航与焦点顺序、高对比度与叙述器验证。

## 硬事实

- 可访问性判据以 **UIA 树实测**为准（Accessibility Insights / Inspect.exe），
  不以「用了语义化控件」的目测代替；断言须给工具与复现步骤。
- 自绘控件（Win32 子类化／`WM_PAINT` 区域）默认不进 UIA 树：须实现
  provider（`IRawElementProviderSimple`）或 WPF `AutomationPeer`，否则屏幕阅读器不可见。
- 只有视觉标签不算名字：`LabeledBy`／助记键（`&File`）须落到 UIA `Name`。
- Tab 顺序与焦点可见性属 blocking：焦点丢失、模态框未闭环、快捷键冲突均可复现。
- 高对比度主题下硬编码颜色即缺陷；须走系统颜色／主题资源。

## 取证命令

```powershell
python -B scripts/os_probe.py --a11y     # 高对比度／叙述器相关系统开关
# Accessibility Insights for Windows（见 dependence/deps.json）人工取证树节点
```

## 边界

文案与视觉层级转 `interface-design-expert`；本叶只裁「是否可达、是否可键盘操作」。

## 相关

[清单](../checklists/accessibility-uia.md) · [上一叶](windowing-dpi-theme.md) ·
[参考书目](../../references/参考书目/参考书目.md)
