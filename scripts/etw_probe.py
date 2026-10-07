"""etw_probe.py — ETW 会话与事件日志可读性取证。

用法：
  python -B scripts/etw_probe.py --sessions        # 活动 ETW 会话（logman）
  python -B scripts/etw_probe.py --providers       # 已注册 provider 概览
  python -B scripts/etw_probe.py --log <通道> --limit N   # 读最近事件
本脚本只读；创建/停止 ETW 会话属系统副作用，须经用户授权后手工执行。
"""
import sys

from _common import flag, has, lines_of, ps

SESSIONS = "logman query -ets 2>$null | Out-String"
PROVIDERS = "(logman query providers 2>$null | Select-Object -First 40) -join '`n'"
LOGTPL = "Get-WinEvent -ListLog '%s' -ErrorAction SilentlyContinue |"
LOGTPL += " Select-Object LogName,IsEnabled,RecordCount,LogType | Format-List"
EVENTS = "$e = Get-WinEvent -LogName '%s' -MaxEvents %d -ErrorAction SilentlyContinue;"
EVENTS += " if (-not $e) { 'no-events-or-denied' } else { $e | Select-Object -First"
EVENTS += " %d | ForEach-Object { $_.TimeCreated.ToString('MM-dd HH:mm:ss') + ' [' "
EVENTS += "+ $_.LevelDisplayName + '] ' + $_.ProviderName + ' ' + $_.Id } }"


def emit(title, script, limit=20):
    """打印一段取证结果，返回码语义：0 有结果／3 不可用。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or ""))
        return 3
    body = lines_of(out)
    if not body:
        print("  EMPTY\t无输出（可能权限不足或通道不存在，须分开归因）")
        return 3
    for line in body[:limit]:
        print("  %s" % line)
    return 0


def main(argv):
    if has(argv, "--sessions"):
        rc = emit("活动 ETW 会话", SESSIONS)
        print("  注意：遗留会话属缺陷，用完须 logman stop -ets <名>")
        return rc
    if has(argv, "--providers"):
        return emit("ETW provider 概览", PROVIDERS, limit=40)
    channel = flag(argv, "--log")
    if channel:
        safe = channel.replace("'", "''")
        limit = int(flag(argv, "--limit", "10") or 10)
        rc = emit("通道元数据: %s" % channel, LOGTPL % safe)
        rc2 = emit("最近事件: %s" % channel, EVENTS % (safe, limit, limit))
        return rc if rc2 == 3 else rc2
    print("用法: etw_probe.py --sessions | --providers | --log <通道> [--limit N]")
    print("建议通道: Application / System / Microsoft-Windows-.../Operational")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
