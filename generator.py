class Generator():
    headers = [
        '#include <bits/stdc++.h>',
        'using namespace std;',
        'double read(){ double d; cin >> d; return d; }',
        'double write(double d){ cout << d; return 0; }',
        'double expt(double base, double powNum){ return pow(base,powNum);}',
        'double expt(double powNum){ return exp(powNum);}'
    ]

    glob_dec = {
        'function': [],
        'constant': []
    }

    code_stream = {
        'main': '', 'function_imp': ''
    }

    s_name = ''

    def write_to_file(self, filename):
        f = open(filename, 'w')
        for header in self.headers:
            f.write(header+'\r\n')

        for constant in self.glob_dec['constant']:
            f.write('const double ')
            f.write(constant.constant_name)
            f.write(' = ')
            f.write(str(constant.number_value))
            f.write(';\r\n')

        for func in self.glob_dec['function']:
            f.write('double ')
            f.write(func.function_name)
            f.write('(')
            params = []
            for param in func.variables.terms:
                params.append(param.identifier_name)
            f.write('double '+',double '.join(params))
            f.write(');\r\n')

        f.write(self.code_stream['main'])
        # self.close_main()
        f.write(self.code_stream['function_imp'])
        f.close()

    # the pregen function will gen the global declaration of a C/C++ code file
    # eg:
    #   const double a = 2000;
    #   double sum(double a, double b);
    # since these global declaration do not need recursion,
    # we can put the entire object in a list, then iteratively
    # write them to files. This will save us from writing multiple pregen
    # for multiple pregen purpose

    def pregen(self, term_names, term):
        self.glob_dec[term_names].append(term)

    # in C/C++, the structure is divided into 3 parts: global declaration,
    # main function, and user-defined functions. Something like this:
    # #include<///>
    # using namespace std;
    #
    # const double A = 20;
    # double func1(double a, double b);
    # void main(){
    # /// something here
    # }
    # double func1(double a, double b){
    #   return a+b
    # }

    # Hence we need functions to handle that 3 main parts

    def start_main(self):
        # set code stream name = main
        self.s_name = 'main'
        self.code_stream[self.s_name] += 'int main(){\r\n'

    def close_main(self):
        self.code_stream[self.s_name] += '\r\n return 0; }'  # close main
        self.s_name = 'function_imp'

    def gen_keyword(self, keyword):  # keywords can be if, else,etc
        self.code_stream[self.s_name] += keyword

    def gen_expt_operator(self, op):
        self.code_stream += 'pow('

    def gen_var(self, variable_name):
        self.code_stream[self.s_name] += 'double '+variable_name+'='
        # no ; here because of the expression

    def gen_number(self, value):
        self.code_stream[self.s_name] += str(value)
