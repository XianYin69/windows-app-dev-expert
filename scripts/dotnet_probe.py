"""dotnet_probe.py — .NET 运行时与 SDK 清单取证（含桌面框架可用性）。

用法：
  python -B scripts/dotnet_probe.py           # SDK／运行时／共享框架
  python -B scripts/dotnet_probe.py --desktop # 桌面共享框架与 .NET Framework
只读枚举，不安装、不改全局配置。
"""
import sys

from _common import has, lines_of, ps, run

DESKTOP = "$p = [Environment]::GetFolderPath('ProgramFiles');"
DESKTOP += "Get-ChildItem -Path (Join-Path $p 'dotnet\\shared') -Directory "
DESKTOP += "-ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name"

LEGACY = "Get-ChildItem 'HKLM:\\SOFTWARE\\Microsoft\\NET Framework Setup\\"
LEGACY += "NDP\\Full' -ErrorAction SilentlyContinue | ForEach-Object {"
LEGACY += " $_.PSChildName + ' ' + (Get-ItemProperty $_.PSPath).Release }"


def show(title, cmd, limit=24):
    """跑一条外部命令并打印关键行；缺可执行记 ABSENT。"""
    print("== %s" % title)
    code, out = run(cmd)
    if code is None:
        print("  ABSENT\t%s（无该 CLI，判据须降级）" % cmd[0])
        return 0
    for line in lines_of(out)[:limit]:
        print("  %s" % line)
    return 1 if code == 0 else 0


def show_ps(title, script, limit=24):
    """跑一段只读 PowerShell 并打印关键行。"""
    print("== %s" % title)
    code, out = ps(script)
    if code != 0:
        print("  UNAVAILABLE\t%s" % (out or ""))
        return 0
    for line in lines_of(out)[:limit]:
        print("  %s" % line)
    return 1


def main(argv):
    if has(argv, "--desktop"):
        hits = show_ps("桌面共享框架", DESKTOP)
        hits += show_ps(".NET Framework（HKLM 只读）", LEGACY)
        return 0 if hits else 3
    hits = 0
    hits += show("dotnet --info", ["dotnet", "--info"])
    hits += show("dotnet --list-sdks", ["dotnet", "--list-sdks"])
    hits += show("dotnet --list-runtimes", ["dotnet", "--list-runtimes"])
    hits += show_ps("桌面共享框架目录", DESKTOP)
    if hits == 0:
        print("降级：无 dotnet CLI，TFM 与运行时判据标 [本地]（见降级策略）")
        return 3
    print("提示：WPF/WinForms 需 net*-windows TFM；跨平台库引用须门控 API")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
