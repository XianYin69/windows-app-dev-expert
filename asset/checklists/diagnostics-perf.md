# diagnostics-perf — 评审清单

- [ ] blocking | 性能结论附采样窗口、机器规格与可复现命令，单次样本不作结论 | etw_probe
- [ ] blocking | ETW 会话用完即停并删除，未遗留 `logman` 会话 | ETW 文档
- [ ] blocking | 崩溃分析有符号来源（PDB／符号服务器），无符号栈标注「待补」 | WinDbg 文档
- [ ] blocking | 事件日志读取失败区分「权限不足」与「通道不存在」两类原因 | wevtutil 文档
- [ ] major | UI 线程无同步阻塞（启动期 I/O、跨线程 `WaitForSingleObject`） | 消息循环文档
- [ ] major | 启动耗时区分冷启动／首次运行（NGEN／ReadyToRun、Defender、策略脚本） | [本地]
- [ ] major | 内存判据给工作集与私有字节两条曲线，未只看任务管理器 | 性能计数器文档
- [ ] major | 掉帧归因区分 UI 线程、DWM 合成与 GPU 驱动版本 | dpi_probe
- [ ] advisory | WER 采集与隐私合规说明（dump 含用户数据） | 平台文档
- [ ] advisory | 长跑进程给出内存增长阈值与看门狗策略 | code-guidelines

## 不可再拓扑声明

「日志与遥测设计」的取证手段与本叶同源（事件日志／ETW），不另立叶。

## 相关

[细则](../knowledge/diagnostics-perf.md) · [知识树](../../references/知识树/知识树.md)
