"""service_probe.py — 服务、计划任务与启动项状态取证（只读）。

用法：
  python -B scripts/service_probe.py --services [名称片段]
  python -B scripts/service_probe.py --tasks
  python -B scripts/service_probe.py --startup
  python -B scripts/service_probe.py            # 三项概览
红线：本脚本只查询，不安装/停止/改启动类型（见注册表与服务安全约束）。
"""
import sys

from _common import flag, has, lines_of, ps

SERVICES = "Get-Service -ErrorAction SilentlyContinue |"
SERVICES += " Group-Object Status | ForEach-Object { $_.Name + '=' + $_.Count };"
SERVICES += "Get-Service -ErrorAction SilentlyContinue | Where-Object {"
SERVICES += " $_.StartType -in @('Automatic','Manual') } | Select-Object -First 25"
SERVICES += " | ForEach-Object { $_.Status + ' ' + $_.StartType + ' ' + $_.Name }"

SERVICES_F = SERVICES.replace("Select-Object -First 25",
                              "Where-Object { $_.DisplayName -like '*%s%' } |"
                              " Select-Object -First 25")

TASKS = "Get-ScheduledTask -ErrorAction SilentlyContinue |"
TASKS += " Where-Object { $_.State -ne 'Disabled' } | Select-Object -First 30 |"
TASKS += " ForEach-Object { $_.State + ' ' + $_.TaskPath + $_.TaskName }"

STARTUP = "Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue |"
STARTUP += " Select-Object -First 25 | ForEach-Object {"
STARTUP += " $_.Name + ' | ' + $_.Command + ' | ' + $_.User + ' | ' + $_.Location }"


def emit(title, script, limit=30):
    """打印一段取证结果：0 有结果／3 不可用。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or ""))
        return 3
    body = lines_of(out)
    for line in body[:limit]:
        print("  %s" % line)
    return 0 if body else 3


def main(argv):
    name = flag(argv, "--name")
    if has(argv, "--services") or name:
        frag = name or (argv[-1] if argv and not argv[-1].startswith("-") else "")
        if frag:
            return emit("服务匹配: %s" % frag, SERVICES_F % frag.replace(
                "'", "''"))
        return emit("服务状态概览", SERVICES)
    if has(argv, "--tasks"):
        return emit("计划任务（未禁用）", TASKS)
    if has(argv, "--startup"):
        return emit("启动项（Win32_StartupCommand）", STARTUP)
    hits = 0
    for title, script in (("服务状态概览", SERVICES),
                          ("计划任务（未禁用）", TASKS),
                          ("启动项", STARTUP)):
        hits += 1 if emit(title, script) == 0 else 0
    if hits == 0:
        print("降级：无只读通道，服务与计划任务判据标 [本地]（见降级策略）")
        return 3
    print("提示：改动服务/计划任务须用户当轮授权并给回滚点")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
