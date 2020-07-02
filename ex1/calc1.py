# Token types
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
TIMES = "TIMES"
DIVIDE = "DIVIDE"
EOF = "EOF"
OPERATOR = "OPERATOR"
OPERATORS = set([PLUS, MINUS, TIMES, DIVIDE])


class Token:
    """Represents the parsed tokens"""

    def __init__(self, type_, value):
        self.type_ = type_  # token type
        self.value = value  # token value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"

    def __repr__(self):
        return self.__str__()

    def is_type(self, type_):
        if self.type_ == type_:
            return True
        if type_ == OPERATOR and self.type_ in OPERATORS:
            return True
        return False


class Interpreter:
    """Tokenizes, parses and executes input code"""

    def __init__(self, text):
        self.text = text  # raw code
        self.pos = 0  # keep track of where we are in the code
        self.current_token = None
        self.current_char = self.text[self.pos]

    def advance(self):
        """advances the cursor in and sets the current character"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """skips over whitespace"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        """tokenize potentially multi-digit integer"""
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return int(num)

    def get_next_token(self):
        """gets the next token in the text"""
        while self.current_char is not None:
            # check if whitespace and if yes skip
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # check if integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())

            # check if operator
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            if self.current_char == "*":
                self.advance()
                return Token(TIMES, "*")
            if self.current_char == "/":
                self.advance()
                return Token(DIVIDE, "/")

            # unknown token
            raise Exception(
                f"Parsing error: Unknown Token, {self.current_char}")

        return Token(EOF, None)

    def check_type(self, expected_type):
        """checks if token is of expected type"""
        if self.current_token.is_type(expected_type):
            return True
        return False

    def eat(self, expected_type):
        """check if token matches expected type and goes to next token if yes"""
        if self.check_type(expected_type):
            self.current_token = self.get_next_token()
        else:
            raise Exception(
                f"parsing error: Unexpected Token, {self.current_token}")

    def term(self):
        """checks and eats an INTEGER token value"""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def operate(self, left_val, right_val, operator):
        """executes parsed operation"""
        if operator.is_type(PLUS):
            return left_val + right_val
        if operator.is_type(MINUS):
            return left_val - right_val
        if operator.is_type(TIMES):
            return left_val * right_val
        if operator.is_type(DIVIDE):
            return left_val / right_val

    def expr(self):
        """parses and executes expression"""
        self.current_token = self.get_next_token()
        result = self.term()
        while self.check_type(OPERATOR):
            operator = self.current_token
            self.eat(OPERATOR)
            result = self.operate(result, self.term(), operator)
        return result


def main():
    while True:
        text = input('calc> ')
        if not text:
            continue
        if text.strip() == "quit":
            break
        if text.strip() == "help":
            print(
                "calculator for the 4 basic arithmetic operations on integers.\n"
                "To quit, type 'quit'.\n"
                "To print this help message, type 'help'.\n"
            )
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
