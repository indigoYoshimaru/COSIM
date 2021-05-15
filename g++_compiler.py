import subprocess

def cpp_execute(cpp_file, exe_file):
    # the first option is the path to the g++ compiler (g++.exe)
    x = subprocess.getoutput(["C:\\Program Files (x86)\\Dev-Cpp\\MinGW64\\bin\\g++.exe", cpp_file, "-o", exe_file])
    if x == "":
        print(subprocess.run(exe_file, capture_output=True).stdout)
    else:
        print(x)
        
cpp_file = open("T:\\1\\2-3\\PPL\\Project\\COSIM\\test.cpp") # path to cpp file
exe_file = open("T:\\1\\2-3\\PPL\\Project\\COSIM\\result.out") # path to the compiled file
cpp_execute(cpp_file.name, exe_file.name)