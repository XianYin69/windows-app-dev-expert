"""os_probe.py — 目标机基线取证：OS 版本／架构／域／shell／已知目录／无障碍开关。

用法：
  python -B scripts/os_probe.py            # 全量基线
  python -B scripts/os_probe.py --shell    # PowerShell 5.1 与 pwsh 7 可用性
  python -B scripts/os_probe.py --paths    # 已知目录实际解析结果
  python -B scripts/os_probe.py --a11y     # 高对比度／叙述器相关开关
  python -B scripts/os_probe.py --domain   # 域加入与策略可见性
只读取证：本脚本不写注册表、不改任何系统状态。
"""
import os
import sys

from _common import has, lines_of, ps, run, which

BASE = "$c = Get-ComputerInfo | Select-Object OsName,OsVersion,OsArchitecture,"
BASE += "WindowsEditionId,OsBuildLab,UserDomain,PartOfDomain;"
BASE += "$c | Format-List | Out-String -Width 200"

SHELL = "(Get-Host).Version.ToString();"
SHELL += "if (Get-Command pwsh -ErrorAction SilentlyContinue) {"
SHELL += " (pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()') }"
SHELL += " else { 'pwsh:absent' }"

PATHS = "$env:APPDATA; $env:LOCALAPPDATA; $env:ProgramData;"
PATHS += "[Environment]::GetFolderPath('CommonApplicationData');"
PATHS += "[Environment]::GetFolderPath('LocalApplicationData')"

A11Y = "Get-ItemProperty 'HKCU:\\Control Panel\\Accessibility' -ErrorAction"
A11Y += " SilentlyContinue | Select-Object HighContrastScheme,ScreenReaderStatus"
A11Y += " | Format-List | Out-String"

DOMAIN = "$cs = Get-CimInstance Win32_ComputerSystem;"
DOMAIN += "'PartOfDomain=' + $cs.PartOfDomain + ' Domain=' + $cs.Domain;"
DOMAIN += "'Elevated=' + ([Security.Principal.WindowsPrincipal]"
DOMAIN += "[Security.Principal.WindowsIdentity]::GetCurrent()"
DOMAIN += ").IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"


def section(title, script):
    """跑一段 PowerShell 并打印结果。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or "powershell 不可用"))
        return 0
    for line in lines_of(out)[:12]:
        print("  %s" % line)
    return 1


def main(argv):
    print("== 进程与运行时")
    print("  python=%s" % sys.version.split()[0])
    print("  arch=%s\tcwd=%s" % (os.environ.get("PROCESSOR_ARCHITECTURE", "?"),
                                 os.getcwd()))
    print("  longpath=%s" % ("MAX_PATH=260 默认，需清单 longPathAware"))
    done = 0
    if has(argv, "--shell"):
        return 0 if section("shell 宿主", SHELL) else 3
    if has(argv, "--paths"):
        return 0 if section("已知目录", PATHS) else 3
    if has(argv, "--a11y"):
        return 0 if section("无障碍开关", A11Y) else 3
    if has(argv, "--domain"):
        return 0 if section("域与提权", DOMAIN) else 3
    code, ver = run(["cmd", "/c", "ver"])
    if code == 0 and ver:
        print("  ver=%s" % lines_of(ver)[0])
    done += section("系统基线", BASE)
    done += section("shell 宿主", SHELL)
    done += section("已知目录", PATHS)
    done += section("无障碍开关", A11Y)
    done += section("域与提权", DOMAIN)
    if which("signtool"):
        print("  signtool=FOUND")
    if done == 0:
        print("降级：判据只能来自静态阅读，须标 [本地] 并给可复现取证命令")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
