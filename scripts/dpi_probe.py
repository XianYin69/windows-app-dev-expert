"""dpi_probe.py — DPI 感知等级与显示器枚举取证。

用法：
  python -B scripts/dpi_probe.py            # 逐显示器 DPI／缩放／工作区
  python -B scripts/dpi_probe.py --theme    # 深浅色与动画相关系统开关（HKCU 只读）
只读取证：DPI 感知等级由应用清单决定，本脚本不改任何全局设置。
"""
import sys

from _common import has, lines_of, ps

MONITORS = "Add-Type -AssemblyName System.Windows.Forms, System.Drawing;"
MONITORS += "$g = [System.Drawing.Graphics]::FromHwnd([IntPtr]::Zero);"
MONITORS += "'SystemDpi=' + $g.DpiX + 'x' + $g.DpiY; $g.Dispose();"
MONITORS += "[System.Windows.Forms.Screen]::AllScreens | ForEach-Object {"
MONITORS += " $_.DeviceName + ' bounds=' + $_.Bounds +"
MONITORS += " ' work=' + $_.WorkingArea }"

THEME = "$p = 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Personalize';"
THEME += "Get-ItemProperty $p -Name AppsUseLightTheme -ErrorAction"
THEME += " SilentlyContinue | Select-Object -ExpandProperty AppsUseLightTheme;"
THEME += "Get-ItemProperty 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion"
THEME += "\\Themes\\Personal' -Name ColorScheme -ErrorAction SilentlyContinue |"
THEME += " Select-Object -ExpandProperty ColorScheme"


def emit(title, script, limit=20):
    """打印一段取证结果：0 有结果／3 不可用。"""
    print("== %s" % title)
    code, out = ps(script)
    if code is None or code != 0:
        print("  UNAVAILABLE\t%s" % (out or ""))
        return 3
    body = lines_of(out)
    if not body:
        print("  EMPTY\t无输出（权限或键不存在，须分开归因）")
        return 3
    for line in body[:limit]:
        print("  %s" % line)
    return 0


def main(argv):
    if has(argv, "--theme"):
        rc = emit("深浅色开关（HKCU 只读）", THEME)
        print("  判据：读取 AppsUseLightTheme=0 判深色；禁止写回该键（注册表约束）")
        return rc
    rc = emit("显示器与 DPI", MONITORS)
    if rc == 0:
        print("  判据：Per-Monitor V2 须在创建窗口前设定，缩放变化处理 WM_DPICHANGED")
    else:
        print("  降级：无 WinForms 取证通道，DPI 判据标 [本地]（见降级策略）")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
