# storage-config — 注册表·配置存储·文件关联

## 判据范围

注册表 hive 与视图（HKCU/HKLM、WOW6432Node）、应用数据目录
（`%APPDATA%`／`%LOCALAPPDATA%`／`ProgramData`／包内 `ApplicationData`）、
文件关联与 URL 协议、配置迁移与敏感数据保护。

## 硬事实

- HKLM 写入需要提权且影响整机：**未经用户明确授权不得建议或执行**
  （见 [注册表与服务安全约束](../../resistance/注册表与服务安全约束/注册表与服务安全约束.md)）。
- 32/64 位视图不同：`HKLM\Software\...` 在 WOW64 下重定向，判据须指明 `KEY_WOW64_64KEY`。
-  roaming（`%APPDATA%`）与本地（`%LOCALAPPDATA%`）语义不同：机器绑定数据放 roaming 会坏。
- 打包应用的 `ApplicationData` 路径与桌面应用不同，且卸载可清除——迁移脚本须分支处理。
- 文件关联的用户选择由 `UserChoice` 保护，程序自写常被拒；协议注册须实测
  `OpenWith` 结果，不得凭注册表写入即断言生效。
- 敏感值不得明文入注册表／配置文件：走 DPAPI／`ProtectedData` 或凭据管理器。

## 取证命令

```powershell
python -B scripts/msix_probe.py          # 当前进程是否有包标识（决定数据目录）
python -B scripts/os_probe.py --paths    # 已知目录实际解析结果
```

## 相关

[清单](../checklists/storage-config.md) · [上一叶](accessibility-uia.md) ·
[ipc-background](ipc-background.md)
