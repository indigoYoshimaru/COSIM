import lexical as lClass

# def add_to_list(l, value):
#     l.append(value)
#     return value


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

            raise Exception("not enough terms", terms)

    return (current_position, lClass.GroupTerm(terms))


def parse_amongs(tokens, position, parse_funcs):
    check_range(position, tokens)

    for funcs in parse_funcs:
        try:
            return funcs(tokens, position)
        except:
            continue

    raise Exception('term not found in list', position)


def parse_token(tokens, position, token_type, text=None):
    check_range(position, tokens)

    current = tokens[position]

    if current.token_type != token_type:
        raise Exception("unexpected token type")

    if text != None and text != current.text:
        raise Exception("token text not match")

    return (position+1, lClass.TokenTerm(current))


def parse_number(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, number_token] = parse_token(
        tokens, current_position, "number", None)

    return (current_position, lClass.NumberExpressionTerm(float(number_token.token.text)))


def parse_identifier(tokens, position):
    check_range(position, tokens)
    current_position = position
    [current_position, identifier_token] = parse_token(
        tokens, current_position, "identifier", None)

    return (current_position, lClass.IdentifierExpressionTerm(identifier_token.token.text))


def parse_defconstant(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defconstant')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    [current_position, number] = parse_number(tokens, current_position)
    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    return (current_position, lClass.DefConstantTerm(identifier.identifier_name, number.value))


def parse_defvar(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'defvar')
    [current_position, identifier] = parse_identifier(tokens, current_position)
    expression=None
    try:
        [current_position, expression] = parse_expression(tokens, current_position)
    except:
        pass

    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")
    return (current_position, lClass.DefVarTerm(identifier.identifier_name, expression))


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
    return (current_position, lClass.DefunTerm(identifier.identifier_name, variables, expression))


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

    return (current_position, lClass.AssignmentStatementTerm(id_token.identifier_name, expression))


def parse_if(tokens, position):
    check_range(position, tokens)
    current_position = position

    [current_position, _] = parse_token(
        tokens, current_position, "literal", "(")
    [current_position, _] = parse_token(
        tokens, current_position, 'keyword', 'if')
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

    [current_position, _] = parse_token(
        tokens, current_position, "literal", ")")

    return (current_position, lClass.IfStatementTerm(condition, statement, else_statement))


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

    return (current_position, lClass.OperatorExpressionTerm(op_token.token.text, left, right))


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

    return (current_position, lClass.FunctionCallExpressionTerm(function_id.identifier_name, params))


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
