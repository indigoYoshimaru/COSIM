# defining all lexical class

# few notes about symbol table:
#   1. although 'if' key word will not be in the symbol table,
#       we need to define scope for its inner statement
space_char = "    "


class Term:
    def value(self):
        return self

    def print_ast(self, level):
        pass

    def print_cst(self, level):
        pass

    def pre_gen_code(self, generator):
        pass

    def gen_main(self, generator):
        pass

    def gen_func(self, generator):
        pass

    def print_symbol(self, sym_tab, level, scope):
        pass


class TokenTerm(Term):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def value(self):
        return self.token

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__,
              self.token.token_type, self.token.text)

    def print_cst(self, level):
        print(space_char*level, self.token.text)

    def pre_gen_code(self, generator):
        pass

    def gen_main(self, generator):
        generator.write_keyword(self.self.token.text)

    def gen_func(self, generator):
        generator.write_keyword(self.self.token.text)

    def print_symbol(self, sym_tab, level, scope):
        pass


class GroupTerm(Term):
    def __init__(self, terms):
        super().__init__()
        self.terms = terms
        self.is_root = False

    def set_is_root(self, value):
        self.is_root = value

    def value(self):
        return self.terms

    def print_ast(self, level):
        if (level == 0):
            print("==========ABSTRACT SYNTAX TREE==========")

        for t in self.terms:
            t.print_ast(level)

    def print_cst(self, level):
        if (level == 0):
            print("==========CONCRETE SYNTAX TREE==========")

        for t in self.terms:
            t.print_cst(level)

    def pre_gen_code(self, generator):
        for t in self.terms:
            t.pre_gen_code(generator)

    def gen_main(self, generator):
        if self.is_root:
            generator.start_main()
            self.set_is_root(False)
        for t in self.terms:
            t.gen_main(generator)

    def gen_func(self, generator):
        if self.is_root:
            generator.close_main()
            self.set_is_root(False)

        for t in self.terms:
            t.gen_func(generator)

    def print_symbol(self, sym_tab, level, scope):
        if (level == 0):
            print("==========SYMBOL TABLE==========")

        for t in self.terms:
            t.print_symbol(sym_tab, level, scope)


class StatementTerm(Term):
    pass


class DefConstantTerm(StatementTerm):
    def __init__(self, constant_name, number_value):
        super().__init__()
        self.constant_name = constant_name
        self.number_value = number_value

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Constant name: ", self.constant_name)
        print(space_char*(level+1), "Value: ", self.number_value)

    def print_cst(self, level):
        print(space_char*level, self.constant_name)
        print(space_char*level, self.number_value)

    def pre_gen_code(self, generator):
        generator.pregen('constant', self)

    def print_symbol(self, sym_tab, level, scope):
        sym_tab.write_table(self.constant_name, 'constant',
                            str(scope)+'-'+str(level))


class DefVarTerm(StatementTerm):
    def __init__(self, variable_name, expression):
        super().__init__()
        self.variable_name = variable_name
        self.expression = expression

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        if self.expression:
            print(space_char*(level+1), "Expression: ")
            self.expression.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.variable_name)
        if self.expression:
            self.expression.print_cst(level+1)

    def gen_main(self, generator):
        generator.gen_var(self.variable_name)
        if self.expression:
            self.expression.gen_main(generator)
        else:
            generator.gen_number(0)
        generator.gen_keyword(';')

    # no gen_func needed here

    def print_symbol(self, sym_tab, level, scope):
        sym_tab.write_table(self.variable_name, 'variable',
                            str(scope)+'-'+str(level))
        # self.expression.print_symbol(sym_tab, level+1)


class DefunTerm(StatementTerm):
    def __init__(self, function_name, variables, statements):
        super().__init__()
        self.function_name = function_name
        self.variables = variables
        self.statements = statements

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Function name: ", self.function_name)
        print(space_char*(level+1), "Parameters:")
        self.variables.print_ast(level+2)
        print(space_char*(level+1), "Statements: ")
        self.statements.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.function_name)
        self.statements.print_cst(level+1)

    def pre_gen_code(self, generator):
        generator.pregen('function', self)

    def gen_func(self, generator):
        generator.gen_keyword('double ')
        generator.gen_keyword(self.function_name)
        generator.gen_keyword('( double ')
        if len(self.variables.terms):
            self.variables.terms[0].gen_func(generator)
            for i in range(1, len(self.variables.terms)):
                generator.gen_keyword(', double ')
                self.variables.terms[i].gen_func(generator)
        generator.gen_keyword('){ return')
        self.statements.gen_func(generator)
        generator.gen_keyword(';}')

    def print_symbol(self, sym_tab, level, scope):
        sym_tab.write_table(self.function_name, 'function',
                            str(scope)+'-'+str(level))
        self.variables.print_symbol(sym_tab, level+1, scope)
        self.statements.print_symbol(sym_tab, level+1, scope)


class AssignmentStatementTerm(StatementTerm):
    def __init__(self,  variable_name, expression):
        super().__init__()
        self.variable_name = variable_name
        self.expression = expression

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ")
        self.expression.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.variable_name)
        # print(space_char*(level), self.variable_name)
        self.expression.print_cst(level+1)

    def gen_main(self, generator):
        generator.gen_keyword(self.variable_name)
        generator.gen_keyword('=')
        self.expression.gen_main(generator)
        generator.gen_keyword(';')

    # no need gen_func here


class IfStatementTerm(StatementTerm):
    def __init__(self, condition, statement, else_statement):
        super().__init__()
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Condition:")
        self.condition.print_ast(level+2)
        print(space_char*(level+1), "True branch:")
        self.statement.print_ast(level+2)
        if self.else_statement != None:
            print(space_char*(level+1), "False branch:")
            self.else_statement.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), "if")
        self.condition.print_cst(level+1)
        self.statement.print_cst(level+1)
        if self.else_statement != None:
            self.else_statement.print_cst(level+1)

    def gen_main(self, generator):
        generator.gen_keyword('if (')
        self.condition.gen_main(generator)
        generator.gen_keyword('){ ')
        self.statement.gen_main(generator)
        generator.gen_keyword('} ')
        if self.else_statement != None:
            generator.gen_keyword('else { ')
            self.else_statement.gen_main(generator)
            generator.gen_keyword('}')

    # no need gen_func here

    def print_symbol(self, sym_tab, level, scope):
        # sym_tab.write_table(self.condition, 'if statement',
        #                     str(scope)+'-'+str(level))
        self.condition.print_symbol(sym_tab, level+1, scope)
        self.statement.print_symbol(sym_tab, level+1, scope)
        if self.else_statement != None:
            self.else_statement.print_symbol(sym_tab, level+1, scope)


class ExpressionTerm(Term):
    pass


class NumberExpressionTerm(ExpressionTerm):
    def __init__(self, value):
        super().__init__
        self.value = value

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__, self.value)

    def print_cst(self, level):
        print(space_char*level, self.value)

    def gen_main(self, generator):
        generator.gen_number(self.value)

    def gen_func(self, generator):
        generator.gen_number(self.value)


class IdentifierExpressionTerm(ExpressionTerm):
    def __init__(self, identifier_name):
        super().__init__
        self.identifier_name = identifier_name

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__, self.identifier_name)

    def print_cst(self, level):
        print(space_char*level, self.identifier_name)

    def gen_main(self, generator):
        generator.gen_keyword(self.identifier_name)

    def gen_func(self, generator):
        generator.gen_keyword(self.identifier_name)

    def print_symbol(self, sym_tab, level, scope):
        sym_tab.write_table(self.identifier_name,
                            'identifier', str(scope)+'-'+str(level))


class OperatorExpressionTerm(ExpressionTerm):
    def __init__(self, operator, left, right):
        super().__init__
        self.operator = operator
        self.left = left
        self.right = right

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Operator: ", self.operator)
        print(space_char*(level+1), "Left expression:")
        self.left.print_ast(level+2)
        print(space_char*(level+1), "Right expression:")
        self.right.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.operator)
        self.left.print_cst(level+1)
        self.right.print_cst(level+1)

    def gen_main(self, generator):
        generator.gen_keyword('(')
        self.left.gen_main(generator)
        generator.gen_keyword(self.operator)  # change this to gen_operator
        self.right.gen_main(generator)
        generator.gen_keyword(')')

    def gen_func(self, generator):
        generator.gen_keyword('(')
        self.left.gen_func(generator)
        generator.gen_keyword(self.operator)
        self.right.gen_func(generator)
        generator.gen_keyword(')')


class FunctionCallExpressionTerm(ExpressionTerm):
    def __init__(self, function_name, params):
        super().__init__
        self.function_name = function_name
        self.params = params

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*level, "Functions name: ", self.function_name)
        print(space_char*(level+1), "Params:")
        if self.params != None:
            self.params.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*level, self.function_name)
        if self.params != None:
            self.params.print_cst(level+1)

    def gen_main(self, generator):
        generator.gen_keyword(self.function_name)
        generator.gen_keyword('(')

        # self.params.gen_main(generator)
        if len(self.params.terms):
            self.params.terms[0].gen_main(generator)

            for i in range(1, len(self.params.terms)):
                generator.gen_keyword(', ')
                self.params.terms[i].gen_main(generator)

        generator.gen_keyword(')')
        if (self.function_name == 'write'):
            generator.gen_keyword(';')

    def gen_func(self, generator):
        if (self.function_name != 'write' and self.function_name != 'read'):
            generator.gen_keyword(self.function_name)
            generator.gen_keyword('( ')
            if len(self.params.terms):
                self.params.terms[0].gen_func(generator)
                for i in range(1, len(self.params.terms)):
                    generator.gen_keyword(', ')
                    self.params.terms[i].gen_func(generator)
            generator.gen_keyword(')')
