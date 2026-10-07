# services-privileges — 评审清单

- [ ] blocking | 未擅自改动系统服务（安装／停止／改启动类型须用户明确授权） | 注册表安全约束
- [ ] blocking | 服务内不弹窗：session 0 隔离，交互走命名管道或独立托盘进程 | 服务文档
- [ ] blocking | 服务登录身份与所需权限匹配，未以 LocalSystem 跑用户态逻辑 | service_probe
- [ ] blocking | 提权方式已指明（清单要求或 `runas`），未声称「进程内自行升权」 | UAC 文档
- [ ] major | 计划任务与服务取舍给出触发器与失败恢复依据 | schtasks 文档
- [ ] major | 企业组策略／AppLocker／杀软白名单经域机实测确认后才给结论 | 企业环境约束
- [ ] major | 令牌与完整性级别假设来自实测（`os_probe --domain`），非默认开发机 | os_probe
- [ ] advisory | 服务卸载路径与残留清理说明完整 | 打包文档
- [ ] advisory | 长时间运行的后台逻辑给出资源上限与看门狗 | code-guidelines
- [ ] advisory | 跨平台守护进程方案不在本叶裁（转 `python-expert`／运维） | dependence

## 不可再拓扑声明

「域策略」与「杀软拦截」共用同一实测手段（目标机执行取证），合并在本叶。

## 相关

[细则](../knowledge/services-privileges.md) · [知识树](../../references/知识树/知识树.md)
