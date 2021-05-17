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
    return result


def print_tokens(tokens):
    print("==========TOKENS=========")
    for token in tokens:
        print(token.text, end=space_char)
    print()
