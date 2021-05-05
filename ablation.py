import re

pattern = re.compile(
    "(?P<keyword>if|defconstant|defvar|defun|setq)\\b|(?P<identifier>[_a-zA-Z][_a-zA-Z0-9]*)\\b|(?P<number>-?([1-9][0-9]*|0)(\\.[0-9]*)?)|(?P<literal>[-\\+\\*/\\(\\)<>=]|/=|[<>]=)|(?P<space>\\s+)|(?P<end>$)|(?P<invalid>.)", re.M | re.S)

space_char = "    "

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


def tokenize(str):
    result = []
    current_token = None
    text = None
    i = 0

    while True:
        m = pattern.match(str, i)
        text = m.group(m.lastgroup)
        current_token = Token(m.lastgroup, text, i)
        i = m.end(m.lastgroup)

        if m.lastgroup == 'space':
            continue

        if m.lastgroup == 'invalid':
            raise InvalidToken(text)

        result.append(current_token)

        if m.lastgroup == 'end':
            return result


class Term:
    def value(self):
        return self

    def print(self, level):
        pass


class TokenTerm(Term):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def value(self):
        return self.token

    def print(self, level):
        print(space_char*level, self.__class__.__name__,
              self.token.token_type, self.token.text)


class GroupTerm(Term):
    def __init__(self, terms):
        super().__init__()
        self.terms = terms

    def value(self):
        return self.terms

    def print(self, level):
        for t in self.terms:
            t.print(level)

class StatementTerm(Term):
    pass


class DefConstantTerm(StatementTerm):
    def __init__(self, contant_name, number_value):
        super().__init__()
        self.contant_name = contant_name
        self.number_value = number_value

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Constant name: ", self.contant_name)
        print(space_char*(level+1), "Value: ", self.number_value)


class DefVarTerm(StatementTerm):
    def __init__(self, variable_name, expression):
        super().__init__()
        self.variable_name = variable_name
        self.expression = expression

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ")
        self.expression.print(level+2)


class DefunTerm(StatementTerm):
    def __init__(self, function_name, variables, statements):
        super().__init__()
        self.function_name = function_name
        self.variables = variables
        self.statements = statements

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Function name: ", self.function_name)
        print(space_char*(level+1), "Statements: ")
        self.statements.print(level+2)




class AssignmentStatementTerm(StatementTerm):
    def __init__(self, variable_name, expression):
        super().__init__()
        self.variable_name = variable_name
        self.expression = expression

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Variable name: ", self.variable_name)
        print(space_char*(level+1), "Expression: ", self.variable_name)
        self.expression.print(level+2)


class IfStatementTerm(StatementTerm):
    def __init__(self, condition, statement, else_statement):
        super().__init__()
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1), "Condition:")
        self.condition.print(level+2)
        print(space_char*(level+1), "True branch:")
        self.statement.print(level+2)
        if self.else_statement != None:
            print(space_char*(level+1), "False branch:")
            self.else_statement.print(level+2)

        


class ExpressionTerm(Term):
    pass


class NumberExpressionTerm(ExpressionTerm):
    def __init__(self, value):
        super().__init__
        self.value = value

    def print(self, level):
        print(space_char*level, self.__class__.__name__, self.value)


class IdentifierExpressionTerm(ExpressionTerm):
    def __init__(self, identifier_name):
        super().__init__
        self.identifier_name = identifier_name

    def print(self, level):
        print(space_char*level, self.__class__.__name__, self.identifier_name)


class OperatorExpressionTerm(ExpressionTerm):
    def __init__(self, operator, left, right):
        super().__init__
        self.operator = operator
        self.left = left
        self.right = right

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*(level+1),"Operator: ", self.operator)
        print(space_char*(level+1), "Left expression:")
        self.left.print(level+2)
        print(space_char*(level+1), "Right expression:")
        self.right.print(level+2)


class FunctionCallExpressionTerm(ExpressionTerm):
    def __init__(self, function_name, params):
        super().__init__
        self.function_name = function_name
        self.params = params

    def print(self, level):
        print(space_char*level, self.__class__.__name__)
        print(space_char*level, "Functions name: ", self.function_name)
        print(space_char*(level+1),"Params:")
        if self.params!=None:
            self.params.print(level+2)


def check_range(position, tokens):
    if position < 0 or position >= len(tokens):
        raise Exception("out of range")


def parse_group(tokens, position, min, max, parse_func):
    current_position = position
    check_range(current_position, tokens)

    if max == 0 or (max < min and max > 0):
        raise Exception("invalid min max range")

    terms = []
    while True:
        try:
            [current_position, current_term] = parse_func(
                tokens, current_position)
            terms.append(current_term)
            if len(terms) < min:
                continue

            if len(terms) == max:
                break
        except:
            if len(terms) >= min:
                break

            raise Exception("not enough terms")

    return (current_position, GroupTerm(terms))


def parse_amongs(tokens, position, parse_funcs):
    check_range(position, tokens)

    for funcs in parse_funcs:
        try:
            return funcs(tokens, position)
        except:
            continue

    raise Exception('term not found in list')


def parse_token(tokens, position, token_type, text=None):
    check_range(position, tokens)

    current = tokens[position]

    if current.token_type != token_type:
        raise Exception("unexpected token type")

    if text != None and text != current.text:
        raise Exception("token text not match")

    return (position+1, TokenTerm(current))


def parse_number(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, number_token] = parse_token(
        tokens, current_position, "number", None)

    return (current_position, NumberExpressionTerm(float(number_token.token.text)))


def parse_identifier(tokens, position):
    check_range(position, tokens)
    current_position=position
    [current_position, identifier_token] = parse_token(
        tokens, current_position, "identifier", None)

    return (current_position, IdentifierExpressionTerm(identifier_token.token.text))


def parse_defconstant(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defconstant')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position, number] = parse_number(tokens, current_position)
    [current_position, _] = parse_token(tokens, current_position, "literal", ")")

    return (current_position, DefConstantTerm(identifier.identifier_name, number.value))


def parse_defvar(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defvar')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position, expression] = parse_expression(tokens, current_position)

    [current_position, _] = parse_token(tokens, current_position, "literal", ")")
    return (current_position, DefVarTerm(identifier.identifier_name, expression))


def parse_defun(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position,_] = parse_token(
        tokens, current_position, 'keyword', 'defun')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position, variables] = parse_group(
        tokens, current_position, 0, -1, parse_identifier)
    [current_position,_] = parse_token(tokens, current_position, "literal", ")")

    [current_position, expression] = parse_expression(tokens, current_position)
    [current_position,_] = parse_token(tokens, current_position, "literal", ")")
    return (current_position, DefunTerm(identifier.identifier_name, variables, expression))


def parse_assignment(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position,_] = parse_token(
        tokens, current_position, 'keyword', 'setq')
    [current_position, id_token] = parse_identifier(tokens, current_position)
    [current_position,  expression] = parse_expression(
        tokens, current_position)
    [current_position,_] = parse_token(tokens, current_position, "literal", ")")

    return (current_position, AssignmentStatementTerm(id_token.identifier_name, expression))


def parse_if(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position,_] = parse_token(tokens, current_position, 'keyword', 'if')
    # [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position, condition] = parse_expression(
        tokens, current_position)
    # [current_position,_] = parse_token(tokens, current_position, "literal", ")")
    [current_position, statement] = parse_statement(tokens, current_position)
    else_statement = None
    try:
        [current_position, else_statement] = parse_statement_expression(
            tokens, current_position)
    except:
        pass

    [current_position,_] = parse_token(tokens, current_position, "literal", ")")

    return (current_position, IfStatementTerm(condition, statement, else_statement))


def parse_operator_expression(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position, op_token] = parse_token(
        tokens, current_position, "literal")

    if op_token.token.text == "(" or op_token.token.text == ")":
        raise Exception("Operator not found")

    [current_position, left] = parse_expression(tokens, current_position)
    [current_position, right] = parse_expression(tokens, current_position)

    [current_position,_] = parse_token(tokens, current_position, "literal", ")")

    return (current_position, OperatorExpressionTerm(op_token.token.text, left, right))


def parse_function_call(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position, function_id] = parse_identifier(
        tokens, current_position)
    [current_position, params] = parse_group(
        tokens, current_position, 0, -1, parse_expression)
    [current_position,_] = parse_token(tokens, current_position, "literal", ")")

    return (current_position, FunctionCallExpressionTerm(function_id.identifier_name, params))


def parse_expression(tokens, position):
    check_range(position, tokens)
    current_position = position
    [current_position, expression] = parse_amongs(tokens, current_position, [ parse_number,
                                                  parse_identifier, parse_function_call, parse_operator_expression, ])

    return [current_position, expression]


def parse_statement_expression(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, expression] = parse_amongs(tokens, current_position, [
                                                  parse_function_call, parse_operator_expression])

    return [current_position, expression]


def parse_statement(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, statement] = parse_amongs(tokens, current_position, [
        parse_defconstant, parse_defvar, parse_defun, parse_if, parse_assignment, parse_statement_expression])

    return (current_position, statement)


def parse_program(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, statements] = parse_group(
        tokens, current_position, 1, -1, parse_statement)
    [current_position,_] = parse_token(tokens, current_position, 'end')

    return (current_position, statements)
