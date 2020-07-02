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
    """Parses and executes input code"""

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

    def parse_integer(self):
        """parses potentially multi-digit integer"""
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return int(num)

    def get_next_token(self):
        """gets and parses the next token in the text"""
        while self.current_char is not None:
            # check if whitespace and if yes skip
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # check if integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.parse_integer())

            # check if operator
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, self.current_char)
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, self.current_char)
            if self.current_char == "*":
                self.advance()
                return Token(TIMES, self.current_char)
            if self.current_char == "/":
                self.advance()
                return Token(DIVIDE, self.current_char)

            # unknown token
            raise Exception(
                f"Parsing error: Unknown Token, {self.current_char}")

        return Token(EOF, None)

    def eat(self, expected_type):
        """check if token matches expected type and goes to next token if yes"""
        if self.current_token.is_type(expected_type):
            self.current_token = self.get_next_token()
            return
        raise Exception(
            f"parsing error: Unexpected Token, {self.current_token}")

    def operate(self, left_val, right_val, operator):
        """executes tokenized operation"""
        if operator.is_type(PLUS):
            return left_val + right_val
        if operator.is_type(MINUS):
            return left_val - right_val
        if operator.is_type(TIMES):
            return left_val * right_val
        if operator.is_type(DIVIDE):
            return left_val / right_val

    def expr(self):
        """tokenizes and executes expression"""
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)
        operator = self.current_token
        self.eat(OPERATOR)
        right = self.current_token
        self.eat(INTEGER)
        return self.operate(left.value, right.value, operator)


def main():
    while True:        
        text = input('calc> ')
        if not text:
            continue
        if text == "quit":
            break
        if text == "help":
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