import os
import sys

def print_exe_path():
    exe_path = os.path.dirname(os.path.realpath(sys.executable))
    print(f"当前exe文件的路径是: {exe_path}")

print_exe_path()
