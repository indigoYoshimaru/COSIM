# main here
from generator import Generator
import compiler_scanner as sc
import ablation as ab
from compiler_parser import parse_program
import input_handler as handler
#input_string = "(if (> 1 2) (+ x 1)(+ x 2) )(defun f (a b c) (+ x 1))(defconstant PI 3.14)"
input_string = handler.handle_input("src1 copy.lisp")
print(input_string)
tokens = sc.tokenize(input_string)
sc.print_tokens(tokens)

[pos, prog1] = parse_program(tokens, 0)
prog1.print_cst(0)
prog1.print_ast(0)
generator = Generator()
prog1.pre_gen_code(generator)
prog1.gen_main(generator)
generator.write_to_file('imsrc.cpp')
