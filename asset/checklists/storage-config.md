# storage-config — 评审清单

- [ ] blocking | 未建议或执行 HKLM 写入；如确需，已获用户明确授权并给回滚点 | 注册表安全约束
- [ ] blocking | 32/64 位注册表视图显式声明（`KEY_WOW64_64KEY`／WOW6432Node） | 注册表文档
- [ ] blocking | 数据目录按打包／非打包分支（`ApplicationData` vs `%APPDATA%`） | msix_probe
- [ ] blocking | 敏感值不明文入注册表／配置（DPAPI／凭据管理器） | [本地]
- [ ] major | roaming 与 local 归属正确：机器绑定数据不放 `%APPDATA%` | 已知目录文档
- [ ] major | 文件关联／协议注册后实测 `OpenWith` 结果，未凭写键即断言生效 | 应用注册文档
- [ ] major | 配置有版本字段与迁移路径，损坏时回退默认而非崩溃 | code-guidelines
- [ ] major | 路径处理遵循命名规则（UNC、长路径、保留名） | 命名文件文档
- [ ] advisory | 卸载残留清理策略（配置／缓存）已说明 | 打包文档
- [ ] advisory | 大规模持久化转专项技能 | dependence

## 不可再拓扑声明

「凭据存储」与 services-privileges 的令牌判据同源，不另立叶。

## 相关

[细则](../knowledge/storage-config.md) · [知识树](../../references/知识树/知识树.md)
