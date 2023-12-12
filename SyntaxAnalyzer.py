


class SyntaxError(Exception):
    def __init__(self, line, token, non_terminal_name, arg="Message unavailable"):
        self.line = line
        self.token = token
        self.non_terminal_name = non_terminal_name
        self.arg = arg
        super().__init__()