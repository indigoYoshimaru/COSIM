import subprocess
import os
dirname = os.path.dirname(__file__)
compiler = os.path.join(dirname, "MinGW64/bin/g++.exe")


def cpp_execute(cpp_file, exe_file):
    x = subprocess.getoutput([compiler, cpp_file, "-o", exe_file])
    if x == "":
        print(subprocess.run(exe_file, capture_output=True).stdout)
    else:
        print(x)


# cpp_execute("test.cpp", "result.out")
