# main here
import scanner as sc
import parser

input_string = "(if (> 1 2) (+ x 1)(+ x 2))(defun f () (+ x 1))(defconstant PI 3.14)"

tokens = sc.tokenize(input_string)

[pos, prog1] = parser.parse_program(tokens,0)
prog1.print_cst(0)
prog1.print_ast(0)