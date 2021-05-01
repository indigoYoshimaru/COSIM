# main here
import ablation as ab
import scanner as sc

input_string = "(if (> 1 2) (+ x 1)(+ x 2))(defun f () (+ x 1))(defconstant PI 3.14)"

tokens = sc.tokenize(input_string)

[pos, prog] = ab.parse_program(tokens, 0)

prog.print(0)

prog