# signing-packaging — 评审清单

- [ ] blocking | 签名结论来自 `Get-AuthenticodeSignature` 与链校验实测，非假设 | sign_probe
- [ ] blocking | 未凭空假设目标机存在可用证书／私钥（HSM 与导出密钥须区分） | 平台假设约束
- [ ] blocking | 签名带 RFC3161 时间戳，证书过期后历史签名仍有效 | Authenticode 文档
- [ ] blocking | MSIX 依赖（框架包／VCL）在目标机就位，安装失败原因已核对 | msix_probe
- [ ] major | 打包模式（MSIX／MSI／绿色）与更新方式一致，未混用留双份安装记录 | 打包文档
- [ ] major | 自动更新有回滚与失败重试，未以管理员静默替换运行中二进制 | UpdateManager 文档
- [ ] major | 安装器不写 HKLM 未经授权的键，卸载清理覆盖配置与服务 | 注册表安全约束
- [ ] major | SmartScreen 与信誉影响已说明，未承诺「签名即免提示」 | 平台文档
- [ ] advisory | 发布产物附校验和与版本对照表 | code-guidelines
- [ ] advisory | 商店分发与企业内部分发路径分开描述 | 部署文档

## 不可再拓扑声明

「证书采购与合规」属流程而非取证手段，不落本技能。

## 相关

[细则](../knowledge/signing-packaging.md) · [知识树](../../references/知识树/知识树.md)
