# ipc-background — 评审清单

- [ ] blocking | 单实例互斥量前缀正确（跨会话用 `Global\`，会话内用 `Local\`） | 同步文档
- [ ] blocking | 提权实例与普通实例的互通场景已实测（不同完整性级别会拒绝连接） | service_probe
- [ ] blocking | 命名管道设了 ACL 且处理 `ERROR_PIPE_BUSY`／断连重连 | 管道文档
- [ ] blocking | 后台通道按形态选择：打包用 `BackgroundTask`，非打包用服务／计划任务 | msix_probe
- [ ] major | 托盘图标隐藏（用户设置）时仍有可达入口，未把「看不见」当失败 | 通知区域文档
- [ ] major | 通知走 Toast／`AppNotification`，未用 MessageBox 冒充通知 | 通知文档
- [ ] major | 开机启动项有卸载清理路径，不留僵尸 `Run` 键 | 企业环境约束
- [ ] major | IPC 消息有版本与长度校验，跨进程升级不破坏兼容 | code-guidelines
- [ ] advisory | 二次实例的「唤起已有窗口」行为明确（`SetForegroundWindow` 限制已考虑） | 平台文档
- [ ] advisory | 并发架构设计转专项技能，本叶只出 Windows 通道判据 | dependence

## 不可再拓扑声明

「通知内容设计」属 interface 层，判据不独立，故不另立叶。

## 相关

[细则](../knowledge/ipc-background.md) · [知识树](../../references/知识树/知识树.md)
