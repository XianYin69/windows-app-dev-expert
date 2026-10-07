# signing-packaging — 代码签名·MSIX/MSI·自动更新

## 判据范围

Authenticode 证书与签名链、时间戳、SmartScreen 与信誉、MSIX／MSI／安装器
（WiX、Inno Setup）、Windows App SDK 部署模式、自动更新与安装检测。

## 硬事实

- 未签名或链不可信的二进制在域机上会被拦；判据须来自
  `Get-AuthenticodeSignature` 的 `Status` 与链校验实测（`sign_probe`），
  **不得凭空假设目标机已有证书或私钥可用**。
- 签名缺时间戳则证书过期后失效；EV 证书影响 SmartScreen 信誉但不保证免提示。
- MSIX 强制签名且校验依赖（`Dependencies` 中的 VCL/框架包版本），
  依赖缺失时安装失败信息常被误读为「包损坏」。
- 打包更新走商店或 `UpdateManager`／重装 MSIX；MSI 走补丁／升级表——
  混用会留双份安装记录，须实测卸载残留。
- 自包含 Windows App SDK 免去框架包但体积大；框架包版本须与目标机已装版本比对。

## 取证命令

```powershell
python -B scripts/sign_probe.py -Path app.exe
python -B scripts/msix_probe.py -PackageFamilyName <fn>
python -B scripts/sdk_probe.py --runtime   # VC++ 运行时与框架包是否就位
```

## 相关

[清单](../checklists/signing-packaging.md) · [上一叶](services-privileges.md) ·
[平台假设约束](../../resistance/平台假设约束/平台假设约束.md)
