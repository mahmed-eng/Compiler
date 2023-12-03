import tkinter as tk
from Operators import Operators
from Keywords import Keywords
from Punctuators import Punctuators
from Separators import Separators
from Identifiers import Identifier
from Constants import Constants

class LexicalError(Exception):
    def __init__(self, line, token):
        self.line = line
        self.token = token
        super().__init__()

class SyntaxError(Exception):
    def __init__(self, line, token, non_terminal_name, arg="Message unavailable"):
        self.line = line
        self.token = token
        self.non_terminal_name = non_terminal_name
        self.arg = arg
        super().__init__()

class Token:
    def __init__(self, value, class_name, line_number):
        self.value = value
        self.class_name = class_name
        self.line_number = line_number

    def generate_str(self):
        return f"value = {self.value}%class = {self.class_name}%line  = {self.line_number}"

    def __str__(self):
        return f"{{\n    value : {self.value}\n    class : {self.class_name}\n    line  : {self.line_number}\n}}\n"

class GenerateTokens:
    token_set = []

    @staticmethod
    def generate(source_data):
        GenerateTokens.token_set = []
        if not source_data.strip():
            GenerateTokens.token_set.append(Token("$$$", "End marker", -1))
            return GenerateTokens.token_set

        current_char, word = "", ""
        line_num = 0
        str_in_prog = char_in_prog = skip_whole_line = False

        for line in source_data.split('\n'):
            line_num += 1
            str_in_prog = char_in_prog = skip_whole_line = False

            i = 0
            while i < len(line):
                skip = False
                current_char = line[i]

                if skip_whole_line:
                    break

                if str_in_prog:
                    if (current_char == "\"" and (line[i - 1] != '\\')) or (i + 1 >= len(line)):
                        word += current_char
                        word = GenerateTokens.create_token(word, line_num)
                        str_in_prog = False
                    else:
                        word += current_char
                    i += 1
                    continue

                elif current_char == "\"" and not char_in_prog:
                    word = GenerateTokens.create_token(word, line_num)
                    word += "\""
                    str_in_prog = True
                    i += 1
                    continue

                if char_in_prog:
                    if (current_char == "'" and (line[i - 1] != '\\')) or (i + 1 >= len(line)):
                        word += current_char
                        word = GenerateTokens.create_token(word, line_num)
                        char_in_prog = False
                    else:
                        word += current_char
                    i += 1
                    continue

                elif current_char == "'":
                    word = GenerateTokens.create_token(word, line_num)
                    word += "'"
                    char_in_prog = True
                    i += 1
                    continue

                if (i + 1 < len(line)) and not str_in_prog:
                    op = line[i:i+2]
                    if Operators.is_multi_character_op(op):
                        word = GenerateTokens.create_token(word, line_num)
                        GenerateTokens.create_token(op, line_num)
                        i += 2
                        skip = True
                    elif current_char == "#" and line[i + 1] == "#":
                        word = GenerateTokens.create_token(word, line_num)
                        skip_whole_line = True
                        break
                    else:
                        i += 1

                # Block for Floating Number
                a = 5
                if current_char == ".":
                    if (i + 1 < len(line)) and int(line[i + 1]) == a:
                        if int(word) == a:
                            word += current_char
                            i += 1
                            continue
                        else:
                            word = GenerateTokens.create_token(word, line_num)
                            word += current_char
                            i += 1
                            continue

                # General Block
                if not skip and not str_in_prog:
                    if GenerateTokens.is_word_breaker(current_char):
                        word = GenerateTokens.create_token(word, line_num)
                        if not Separators.is_separator(current_char):
                            GenerateTokens.create_token(current_char, line_num)
                    else:
                        word += current_char
                    i += 1

            if word:
                GenerateTokens.create_token(word, line_num)

        GenerateTokens.token_set.append(Token("$$$", "End marker", -1))
        return GenerateTokens.token_set

    @staticmethod
    def create_token(word, line_num):
        if word:
            class_part = GenerateTokens.calculate_class_name(word)
            if class_part == "[error]: Unknown type":
                raise LexicalError(line_num, word)
            GenerateTokens.token_set.append(Token(word, class_part, line_num))
        return ""

    @staticmethod
    def is_word_breaker(char):
        return Operators.is_operator(char) or Punctuators.is_punctuator(char) or Separators.is_separator(char)

    @staticmethod
    def calculate_class_name(word):
        if Keywords.is_keyword(word):
            return Keywords.get_keyword_class_name(word)
        elif Operators.is_operator(word):
            return Operators.get_operator_class_name(word)
        elif Punctuators.is_punctuator(word):
            return Punctuators.get_punctuator_class_name(word)
        elif Constants.is_constant(word):
            return Constants.get_constant_class_name(word)
        elif Identifier.is_identifier(word):
            return "Identifier"

        return "[error]: Unknown type"

def append_text(widget, text, color):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, text, color)
    widget.config(state=tk.DISABLED)

# GUI setup
def on_generate_tokens():
    debug_window.config(state=tk.NORMAL)
    debug_window.delete("1.0", tk.END)
    debug_window.config(state=tk.DISABLED)

    code_text = code_area.get("1.0", tk.END).strip()
    try:
        token_list = GenerateTokens.generate(code_text)
        if token_list is not None:
            # Perform actions with token_list as needed
            append_text(debug_window, "[Lexical Error] No Lexical error found. \n", "green")
    except LexicalError as e:
        append_text(debug_window, f"[Lexical Error] Token doesn't meet language specification at\nline number: {e.line}\ntoken: \"{e.token}\"", "red")

root = tk.Tk()
root.title("Token Generator")

code_area = tk.Text(root, wrap="word", width=65, height=35)
code_area.pack(padx=10, pady=10)

generate_button = tk.Button(root, text="Generate Tokens", command=on_generate_tokens)
generate_button.pack(pady=10)

debug_window = tk.Text(root, wrap="word", width=65, height=10)
debug_window.pack(pady=10)

root.mainloop()