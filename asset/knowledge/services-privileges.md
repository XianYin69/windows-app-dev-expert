# services-privileges — 服务·计划任务·UAC 提权

## 判据范围

SCM 与 Windows 服务（安装／恢复／登录身份）、计划任务、UAC 与提权路径、
令牌与完整性级别、企业策略（组策略／AppLocker／杀软白名单）。

## 硬事实

- 服务运行在 session 0，与用户桌面隔离：服务内弹窗属缺陷设计，判据须引
  交互式通道（命名管道／托盘进程）替代方案。
- 服务登录身份决定可见资源（网络凭据、HKCU 归属）；以 LocalSystem 跑
  用户态逻辑即权限越界。
- 提权路径只有 `runas`（`ShellExecuteEx` + `SEE_MASK`）与清单要求两种，
  进程内无法自行升权；断言「自动以管理员运行」须指明实现方式。
- 计划任务与服务的差别在触发器与失败恢复，schtasks 与 `Get-ScheduledTask`
  结果须实测，不得凭模板推断。
- **企业环境组策略／AppLocker／杀软白名单必须实测确认**：同一二进制在
  域机上可能被直接拦停（见 [企业环境约束](../../resistance/企业环境约束/企业环境约束.md)）。

## 取证命令

```powershell
python -B scripts/service_probe.py --services
python -B scripts/service_probe.py --tasks
python -B scripts/os_probe.py --domain    # 域 joined／策略可见性
```

## 相关

[清单](../checklists/services-privileges.md) · [上一叶](ipc-background.md) ·
[signing-packaging](signing-packaging.md)
