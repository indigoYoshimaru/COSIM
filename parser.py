import lexical as lClass

pattern = re.compile(
    "(?P<keyword>if|defconstant|defvar|defun|setq)\\b|(?P<identifier>[_a-zA-Z][_a-zA-Z0-9]*)\\b|(?P<number>-?([1-9][0-9]*|0)(\\.[0-9]*)?)|(?P<literal>[-\\+\\*/\\(\\)<>=]|/=|[<>]=)|(?P<space>\\s+)|(?P<end>$)|(?P<invalid>.)", re.M | re.S)

space_char = "    "

# class Node():
#     def __init__(self):
#         self.left_child = None
#         self.right_child = None
#         self.value = None
#         self.level = None


def add_to_list(l, value):
    l.append(value)
    return value


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
    current_position = position
    [current_position, identifier_token] = parse_token(
        tokens, current_position, "identifier", None)

    return (current_position, IdentifierExpressionTerm(identifier_token.token.text))


def parse_defconstant(tokens, position):
    check_range(position, tokens)
    current_position = position

    values = []

    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, "literal", "("))
    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, 'keyword', 'defconstant'))
    [current_position, identifier] = add_to_list(
        values, parse_identifier(tokens, current_position))
    [current_position, number] = add_to_list(
        values, parse_number(tokens, current_position))
    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, "literal", ")"))

    return (current_position, DefConstantTerm(values, identifier.identifier_name, number.value))


def parse_defvar(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defvar')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position, expression] = parse_expression(tokens, current_position)

    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")
    return (current_position, DefVarTerm(identifier.identifier_name, expression))


def parse_defun(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defun')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, variables] = parse_group(
        tokens, current_position, 0, -1, parse_identifier)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    [current_position, expression] = parse_expression(tokens, current_position)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")
    return (current_position, DefunTerm(identifier.identifier_name, variables, expression))


def parse_assignment(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'setq')
    [current_position, id_token] = parse_identifier(tokens, current_position)
    [current_position,  expression] = parse_expression(
        tokens, current_position)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    return (current_position, AssignmentStatementTerm(id_token.identifier_name, expression))


def parse_if(tokens, position):
    check_range(position, tokens)
    current_position = position

    values = []

    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, "literal", "("))
    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, 'keyword', 'if'))
    # [current_position,_] = parse_token(tokens, current_position, "literal", "(")
    [current_position, condition] = add_to_list(values, parse_expression(
        tokens, current_position))
    # [current_position,_] = parse_token(tokens, current_position, "literal", ")")
    [current_position, statement] = add_to_list(
        values, parse_statement(tokens, current_position))
    else_statement = None
    try:
        [current_position, else_statement] = add_to_list(values, parse_statement_expression(
            tokens, current_position))
    except:
        pass

    [current_position, _] = add_to_list(values, parse_token(
        tokens, current_position, "literal", ")"))

    return (current_position, IfStatementTerm(values, condition, statement, else_statement))


def parse_operator_expression(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, op_token] = parse_token(
        tokens, current_position, "literal")

    if op_token.token.text == "(" or op_token.token.text == ")":
        raise Exception("Operator not found")

    [current_position, left] = parse_expression(tokens, current_position)
    [current_position, right] = parse_expression(tokens, current_position)

    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    return (current_position, OperatorExpressionTerm(op_token.token.text, left, right))


def parse_function_call(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, function_id] = parse_identifier(
        tokens, current_position)
    [current_position, params] = parse_group(
        tokens, current_position, 0, -1, parse_expression)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    return (current_position, FunctionCallExpressionTerm(function_id.identifier_name, params))


def parse_expression(tokens, position):
    check_range(position, tokens)
    current_position = position
    [current_position, expression] = parse_amongs(tokens, current_position, [parse_number,
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
    [current_position, _] = parse_token(tokens, current_position, 'end')

    return (current_position, statements)


if __name__ == "__main__":
    import scanner
    input_string = "(if (> 1 2) (+ x 1)(+ x 2))(defun f () (+ x 1))(defconstant PI 3.14)"
    tokens = scanner.tokenize(input_string)
    for token in tokens:
        print(token.text, end='  ')
    print(parse_token(tokens, 1,))
