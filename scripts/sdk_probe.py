"""sdk_probe.py — Windows SDK 与 MSVC 工具集取证（vswhere／头文件／lib／工具）。

用法：
  python -B scripts/sdk_probe.py            # 工具集与 SDK 概览
  python -B scripts/sdk_probe.py --runtime  # VC++ 可再发行运行时清单
  python -B scripts/sdk_probe.py --tools    # signtool/makeappx/dumpbin/cdb 等
本脚本只读枚举，不触发安装。
"""
import glob
import os
import sys

from _common import has, lines_of, ps, run, which

VSWHERE = os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                       "Microsoft Visual Studio", "Installer", "vswhere.exe")

VS_QUERY = "& '%s' -all -products * -format value -property " % VSWHERE
VS_QUERY += "'installationPath' -version '[16.0,)'"

RUNTIMES = "Get-ChildItem 'HKLM:\\SOFTWARE\\Microsoft\\"
RUNTIMES += "VisualStudio\\14.0\\VC\\Runtimes' -ErrorAction SilentlyContinue |"
RUNTIMES += " ForEach-Object { $_.PSChildName + ' ' + "
RUNTIMES += "(Get-ItemProperty $_.PSPath).Version }"

SDKS = "Get-ChildItem 'HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\"
SDKS += "Windows Kits\\Installed Products' -ErrorAction SilentlyContinue |"
SDKS += " Select-Object -ExpandProperty PSChildName | Select-String -Pattern 'SDK'"

TOOLS = ("signtool", "makeappx", "dumpbin", "cl", "link", "cmake", "cdb",
         "xperf", "PerfView", "mt", "rc", "msbuild", "nuget", "dotnet")


def probe_tools():
    """枚举依赖工具是否在 PATH。"""
    found = 0
    for name in TOOLS:
        exe = which(name)
        print("%-12s %s\t%s" % (name, "FOUND" if exe else "ABSENT",
                                exe or "-"))
        if exe:
            found += 1
    return found


def probe_kit_dirs():
    """枚举 Windows Kits 目录与 SDK 头文件根。"""
    root = os.path.join(os.environ.get("ProgramFiles(x86)",
                                       r"C:\Program Files (x86)"),
                        "Windows Kits", "10")
    if not os.path.isdir(root):
        print("Windows Kits 10\tABSENT")
        return 0
    inc = sorted(glob.glob(os.path.join(root, "Include", "*")))
    lib = sorted(glob.glob(os.path.join(root, "Lib", "*")))
    print("Windows Kits 10\tFOUND")
    for item in inc[-3:]:
        print("  include\t%s" % os.path.basename(item))
    for item in lib[-3:]:
        print("  lib\t%s" % os.path.basename(item))
    return 1


def main(argv):
    hits = 0
    if has(argv, "--runtime"):
        code, out = ps(RUNTIMES)
        print("== VC++ 运行时（HKLM 只读枚举）")
        for line in lines_of(out) if code == 0 else ["UNAVAILABLE", out or ""]:
            print("  %s" % line)
        return 0 if code == 0 else 3
    if has(argv, "--tools"):
        print("== PATH 工具探测")
        return 0 if probe_tools() else 3
    print("== Visual Studio 安装（vswhere）")
    if not os.path.exists(VSWHERE):
        print("  vswhere ABSENT\t%s" % VSWHERE)
    else:
        code, out = ps(VS_QUERY)
        for line in lines_of(out) if code == 0 else ["  UNAVAILABLE"]:
            print("  %s" % line)
        hits += 1 if code == 0 else 0
    print("== Windows SDK 目录")
    hits += probe_kit_dirs()
    code, out = ps(SDKS)
    if code == 0:
        for line in lines_of(out)[:6]:
            print("  installed\t%s" % line)
    print("== PATH 工具探测")
    hits += probe_tools()
    if hits == 0:
        print("降级：无 MSVC/SDK，编译与打包判据只能标 [本地]（见降级策略）")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
