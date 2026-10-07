# diagnostics-perf — ETW·事件日志·崩溃 dump·性能

## 判据范围

ETW 会话与 provider、Windows 事件日志与 WER、崩溃 dump 采集与 WinDbg 分析、
启动耗时、内存与工作集、GPU／DWM 合成与掉帧。

## 硬事实

- 性能结论只来自可复现测量（ETW/xperf/PerfView/计数器），且须给采样窗口与机器规格；
  「感觉变快」不作 blocking 判据。
- 事件日志读取受权限限制（Admin／Operational 通道常需提权），
  `Get-WinEvent` 失败要区分权限与通道不存在两种原因。
- ETW 会话是共享资源：`logman` 创建后必须停止并删除，遗留会话即缺陷。
- dump 分析须符号（PDB／微软符号服务器）；无符号的栈只能给「待补符号」结论。
- 启动耗时须区分冷启动／首次运行（NGEN／ReadyToRun、Defender 扫描、
  组策略脚本）；单一样本不得升为结论。
- UI 线程阻塞（同步等待、启动期 I/O）是掉帧与「未响应」的首要嫌疑，
  判据须给消息循环内的可复现证据。

## 取证命令

```powershell
python -B scripts/etw_probe.py --sessions
python -B scripts/etw_probe.py --log Application --limit 20
python -B scripts/dpi_probe.py            # 显示器与合成环境（GPU 相关）
```

## 相关

[清单](../checklists/diagnostics-perf.md) · [上一叶](signing-packaging.md) ·
[降级策略](../../resistance/降级策略/降级策略.md)
