# ipc-background — 单实例·IPC·托盘·后台任务

## 判据范围

单实例（互斥量／本地命名对象）、进程间通信（命名管道／`WM_COPYDATA`／内存映射／
App Service）、托盘图标与通知（Toast）、开机启动与后台任务。

## 硬事实

- 单实例互斥量须区分 `Local\` 与 `Global\` 前缀：跨会话（服务与桌面、多用户）
  用 `Local\` 即失效；判据须给会话与提权两种场景的实测。
- 命名管道须处理 `ERROR_PIPE_BUSY` 与消息模式／字节模式差异；未设 ACL 即
  暴露本机任意进程可连——安全判据须引 ACL 实测。
- 托盘图标属通知区域（`Shell_NotifyIcon`），用户可在设置中隐藏；
  「看不到图标」不等于功能失败，须查 `NotifyIcon` 可见性策略。
- 开机启动有注册表 `Run` 键、启动文件夹、计划任务、后台任务四类，
  企业环境可能被组策略禁用——断言前须实测（`service_probe`）。
- 打包应用的后台任务走 `BackgroundTask`／`ApplicationTrigger`，
  非打包应用无此通道，须改用服务或计划任务。

## 取证命令

```powershell
python -B scripts/service_probe.py       # 服务／计划任务／启动项状态
python -B scripts/msix_probe.py          # 是否打包（决定后台任务通道）
```

## 相关

[清单](../checklists/ipc-background.md) · [上一叶](storage-config.md) ·
[services-privileges](services-privileges.md)
