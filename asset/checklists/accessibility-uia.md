# accessibility-uia — 评审清单

- [ ] blocking | 自绘控件已实现 UIA provider／`AutomationPeer`，屏幕阅读器可读 | UIA 文档
- [ ] blocking | 每个可交互元素有非空 UIA `Name`（视觉标签不等于名字） | 无障碍文档
- [ ] blocking | 键盘可达：Tab 顺序合理、焦点可见、模态框焦点闭环 | [本地]
- [ ] blocking | 断言来自 Accessibility Insights／Inspect 实测，非目测 | 工具清单
- [ ] major | 控件模式选择正确（Invoke/Value/SelectionItem/Toggle） | UIA 文档
- [ ] major | 高对比度主题下无硬编码颜色，走系统颜色资源 | 平台文档
- [ ] major | 触发操作不只依赖悬停；快捷键无冲突 | 无障碍文档
- [ ] major | 图标按钮有 `AutomationId` 或本地化 `Name`，动态内容变更发通知 | UIA 文档
- [ ] advisory | 文本缩放与最小点击区域给出建议值 | 无障碍文档
- [ ] advisory | 文案与视觉层级转 `interface-design-expert` | dependence

## 不可再拓扑声明

「本地化文本可读性」落在本叶与 storage-config 的 roaming 判据内，不另立叶。

## 相关

[细则](../knowledge/accessibility-uia.md) · [知识树](../../references/知识树/知识树.md)
