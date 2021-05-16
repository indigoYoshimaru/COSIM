# defining all lexical class

space_char = "    "


class Term:
    def value(self):
        return self

    def print_ast(self, level):
        pass

    def print_cst(self, level):
        pass

    def pre_gen_code(self, writer):
        pass

    def gen_code(self, writer):
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


class StatementTerm(Term):
    pass


class DefConstantTerm(StatementTerm):
    def __init__(self, contant_name, number_value):
        super().__init__()
        self.contant_name = contant_name
        self.number_value = number_value

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Constant name: ", self.contant_name)
        print(space_char*(level+1), "Value: ", self.number_value)

    def print_cst(self, level):
        print(space_char*level, self.contant_name)
        print(space_char*level, self.number_value)


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

    def gen_func(self, generator):
        generator.gen_keyword(self.variable_name)
        if self.expression:
            generator.gen_keyword('=')
            self.expression.gen_func(generator)



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

    def gen_func(self,generator):
        generator.gen_keyword(self.function_name)
        generator.gen_keyword('(')
        self.variables.gen_func(generator)
        generator.gen_keyword('){ return')
        self.statements.gen_func(generator)
        generator.gen_keyword(';}')



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

    def gen_main(self,generator):
        generator.gen_keyword(self.variable_name)
        generator.gen_keyword('=')
        self.expression.gen_main(generator)
        generator.gen_keyword(';')

    def gen_func(self, generator):
        generator.gen_keyword(self.variable_name)
        generator.gen_keyword('=')
        self.expression.gen_main(generator)


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
        #print(space_char*(level), "then")
        self.statement.print_cst(level+1)
        #print(space_char*(level), "else")
        if self.else_statement != None:
            self.else_statement.print_cst(level+1)


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
        if (self.operator=='expt'):
            generator.gen_operator('pow(')
            self.left.gen_main(generator)
            generator.gen_keyword(', ')
            self.right.gen_main(generator)
            generator.gen_keyword(')')
        else:
            generator.gen_keyword('(') 
            self.left.gen_main(generator)
            generator.gen_operator(self.operator)# change this to gen_operator
            self.right.gen_main(generator)
            generator.gen_keyword(')') 

    def gen_func(self, generator):
        if (self.operator=='expt'):
            generator.gen_operator('pow(')
            self.left.gen_func(generator)
            generator.gen_keyword(', ')
            self.right.gen_func(generator)
            generator.gen_keyword(')')
        else:
            generator.gen_keyword('(') 
            self.left.gen_func(generator)
            generator.gen_operator(self.operator)# change this to gen_operator
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

    def gen_main(self, generator): #params co the la ham, bien hoac so D:   
        generator.gen_keyword(self.function_name)
        generator.gen_keyword('( ')

        #self.params.gen_main(generator)
        if len(self.params.terms):
            self.params.terms[0].gen_main(generator)
            
            for i in range(1, len(self.params.terms)):
                generator.gen_keyword(', ')
                self.params.terms[i].gen_main(generator)

        

        generator.gen_keyword(')')

    def gen_func(self, generator):
        generator.gen_keyword(self.function_name)
        generator.gen_keyword('( ')
        if len(self.params.terms):
            self.params.terms[0].gen_func(generator)
            for i in range(1, len(self.params.terms)):
                generator.gen_keyword(', ')
                self.params.terms[i].gen_func(generator)
