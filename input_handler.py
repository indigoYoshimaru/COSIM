def handle_input(file_path):
    import re
    code = open(file_path).read().split("\n")
    code = [exp[: (len(exp)) if exp.find(";") == -1 else exp.index(";")] for exp in code]
    code = [exp.strip() for exp in code]
    code = [exp for exp in code if exp != ""]
    code = " ".join(code)
    code = re.sub(re.compile("#\|.*?\|#", re.DOTALL), "", code)
    code = re.sub(re.compile("\|#?.*\|#", re.DOTALL), "", code)
    code = " ".join(code.split())
    return code

codestream = handle_input("T:\\1\\2-3\\PPL\\Project\\COSIM\\program.lisp")
print(codestream)