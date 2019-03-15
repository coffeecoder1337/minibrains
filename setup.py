from cx_Freeze import setup, Executable

setup(
    name = "MiniBrains",
    version = "1.0",
    description = "MiniBrains",
    executables = [Executable("main.py")]
)