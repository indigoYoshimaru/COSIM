# defining all lexical class

from os import get_terminal_size


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

    def print_symbol(self, sym_tab, level):
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


class GroupTerm(Term):
    def __init__(self, terms):
        super().__init__()
        self.terms = terms

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
        generator.start_main()
        for t in self.terms:
            t.gen_main(generator)

    def gen_func(self, generator):
        generator.close_main()
        for t in self.terms:
            t.gen_func(generator)


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


class DefVarTerm(StatementTerm):
    def __init__(self, variable_name, expression):
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
        self.expression.print_cst(level+1)


class DefunTerm(StatementTerm):
    def __init__(self, function_name, variables, statements):
        super().__init__()
        self.function_name = function_name
        self.variables = variables
        self.statements = statements

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Function name: ", self.function_name)
        print(space_char*(level+1), "Statements: ")
        self.statements.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.function_name)
        self.statements.print_cst(level+1)

    def pre_gen_code(self, generator):
        generator.pregen('function', self)


class AssignmentStatementTerm(StatementTerm):
    def __init__(self,  variable_name, expression):
        super().__init__()
        self.variable_name = variable_name
        self.expression = expression

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ", self.variable_name)
        self.expression.print_ast(level+2)

    def print_cst(self, level):
        print(space_char*(level), self.variable_name)
        print(space_char*(level), self.variable_name)
        self.expression.print_cst(level+1)


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
        if self.else_statement != None:
            generator.gen_keyword('} else { ')
            self.else_statement.gen_main(generator)
            generator.gen_keyword('}')


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
        self.left.gen_main(generator)
        generator.gen_keyword(self.operator)# change this to gen_operator
        self.right.gen_main(generator)

        if (self.operator=='expt'):
            generator.gen_operator()


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
