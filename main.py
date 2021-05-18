# main here
from typing import Pattern
from generator import Generator
import compiler_scanner as sc
from compiler_parser import parse_program
import input_handler as handler
from symbol_table import SymbolTable
import re
import argparse
import cpp_compiler

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input file directory')
args = vars(parser.parse_args())
split_file_dir = re.split("[\b\W\b]+", args['input'])
file_name = split_file_dir[len(split_file_dir)-2]
print('Your file name is :', file_name)

input_string = handler.handle_input(args['input'])
print('Code string after handling:', input_string)
tokens = sc.tokenize(input_string)
sc.print_tokens(tokens)

[pos, prog1] = parse_program(tokens, 0)
prog1.print_cst(0)
prog1.print_ast(0)
sym_table = SymbolTable()
prog1.print_symbol(sym_table, 0, 0)
sym_table.visualize()
generator = Generator()
prog1.pre_gen_code(generator)
prog1.set_is_root(True)
prog1.gen_main(generator)
prog1.set_is_root(True)
prog1.gen_func(generator)
generator.write_to_file('outfiles\\'+file_name+'.cpp')
cpp_compiler.cpp_execute('outfiles\\'+file_name+'.cpp',
                         'outfiles\\res_'+file_name+'.out')
