import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "include_files": "parsers",
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="stumpblock",
    version="1.0.0-beta",
    description="Converts C# code to flow charts",
    options={
        "build_exe": build_exe_options,
    },
    executables=[Executable("main.py", target_name="stumpblock", base=base)],
)
