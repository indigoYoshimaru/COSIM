# defining all lexical class

class Token:
    def __init__(self, token_type, text, position):
        super().__init__
        self.token_type = token_type
        self.text = text
        self.position = position


class InvalidToken(Exception):
    def __init__(self, text, position):
        super().__init__
        self.text = text
        self.position = position


class Term:
    def __init__(self, tokens_positions):
        self.tokens_positions = tokens_positions

    def value(self):
        return self

    def print_ast(self, level):
        pass

    def print_cst(self, level):
        pass


class TokenTerm(Term):
    def __init__(self, tokens_positions, token):
        super().__init__(tokens_positions)
        self.token = token

    def value(self):
        return self.token

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__,
              self.token.token_type, self.token.text)


class GroupTerm(Term):
    def __init__(self, tokens_positions, terms):
        super().__init__(tokens_positions)
        self.terms = terms

    def value(self):
        return self.terms

    def print_ast(self, level):
        for t in self.terms:
            t.print_ast(level)


class StatementTerm(Term):
    pass


class DefConstantTerm(StatementTerm):
    def __init__(self, tokens_positions, contant_name, number_value, tokens_positions):
        super().__init__(tokens_positions)
        self.contant_name = contant_name
        self.number_value = number_value

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Constant name: ", self.contant_name)
        print(space_char*(level+1), "Value: ", self.number_value)

    def print_cst(self, level):
        print(space_char*level, self.__class__.__name__)
        for [pos, token] in self.tokens_positions:
            token.print_cst(level+1)


class DefVarTerm(StatementTerm):
    def __init__(self, tokens_positions, variable_name, expression):
        super().__init__(tokens_positions)
        self.variable_name = variable_name
        self.expression = expression

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ")
        self.expression.print_ast(level+2)


class DefunTerm(StatementTerm):
    def __init__(self, tokens_positions, function_name, variables, statements):
        super().__init__(tokens_positions)
        self.function_name = function_name
        self.variables = variables
        self.statements = statements

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Function name: ", self.function_name)
        print(space_char*(level+1), "Statements: ")
        self.statements.print_ast(level+2)


class AssignmentStatementTerm(StatementTerm):
    def __init__(self, tokens_positions, variable_name, expression):
        super().__init__(tokens_positions)
        self.variable_name = variable_name
        self.expression = expression

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ", self.variable_name)
        self.expression.print_ast(level+2)


class IfStatementTerm(StatementTerm):
    def __init__(self, tokens_positions, condition, statement, else_statement):
        super().__init__(tokens_positions)
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Condition:")
        self.condition.print(level+2)
        print(space_char*(level+1), "True branch:")
        self.statement.print(level+2)
        if self.else_statement != None:
            print(space_char*(level+1), "False branch:")
            self.else_statement.print_ast(level+2)


class ExpressionTerm(Term):
    pass


class NumberExpressionTerm(ExpressionTerm):
    def __init__(self, tokens_positions, value):
        super().__init__
        self.value = value

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__, self.value)


class IdentifierExpressionTerm(ExpressionTerm):
    def __init__(self, tokens_positions, identifier_name):
        super().__init__
        self.identifier_name = identifier_name

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__, self.identifier_name)


class OperatorExpressionTerm(ExpressionTerm):
    def __init__(self, tokens_positions, operator, left, right):
        super().__init__
        self.operator = operator
        self.left = left
        self.right = right

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Operator: ", self.operator)
        print(space_char*(level+1), "Left expression:")
        self.left.print(level+2)
        print(space_char*(level+1), "Right expression:")
        self.right.print_ast(level+2)


class FunctionCallExpressionTerm(ExpressionTerm):
    def __init__(self, tokens_positions, function_name, params):
        super().__init__
        self.function_name = function_name
        self.params = params

    def print_ast(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*level, "Functions name: ", self.function_name)
        print(space_char*(level+1), "Params:")
        if self.params != None:
            self.params.print_ast(level+2)
