# platform-selection — 评审清单

判据写法：`- [ ] 级别 | 判据 | 出处`。级别 blocking > major > advisory。

- [ ] blocking | 已指明目标形态（Win32／UWP／WinUI 3＋Windows App SDK）与打包模式 | 官方文档
- [ ] blocking | 断言依赖的 API 在目标 Windows 版本可用（给构建号与取证命令） | os_probe
- [ ] blocking | 非打包进程未调用需包标识的 API（或已给出包标识实测结果） | msix_probe
- [ ] blocking | UWP 的 `Windows.UI.Xaml` 未被当作演进中的 UI 层推荐 | 平台文档
- [ ] major | Windows App SDK 部署模式（框架包／自包含）已选定并说明取舍 | 部署文档
- [ ] major | 框架包版本与目标机已装版本比对过（缺版本即安装失败） | msix_probe
- [ ] major | COM／WinRT 边界错误按 `HRESULT` 检查，未只依赖异常投影 | COM 文档
- [ ] major | 选型结论区分了「企业策略限制」与「技术限制」两类原因 | 企业环境约束
- [ ] advisory | 迁移路径（UWP→WinUI 3）给出分阶段与回退点 | 迁移文档
- [ ] advisory | 未把团队偏好写成平台约束 | code-guidelines

## 不可再拓扑声明

「打包身份」「框架包依赖」的判据均落在本叶与 signing-packaging 两叶内，
不构成独立取证手段，故不另立叶。

## 相关

[细则](../knowledge/platform-selection.md) · [知识树](../../references/知识树/知识树.md)
