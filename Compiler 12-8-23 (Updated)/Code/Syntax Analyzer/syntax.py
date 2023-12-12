import tkinter as tk
from tkinter import filedialog
import re

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        process_file(file_path)

def process_file(file_path):
    with open(file_path, 'r') as file:
        programming_syntax = file.read()

    # Tokenization based on the provided pattern
    token_pattern = [
        (r'\+\+', 'inc_dec_op'),
        (r'--', 'dec_op'),
        (r'\+\+=', 'assign_op'),
        (r'=', 'assign_op'),
        (r'==', 'comp_op'),
        (r'!=', 'comp_op'),
        (r'\+', 'arith_op'),
        (r'-', 'arith_op'),
        (r'!', 'not_op'),
        (r'for|if|else-if|while', 'keyword'),
        (r'"[^"]*"', 'String'),
        (r"'[a-zA-Z]'", 'char'),
        (r'//.*', 'single_line_comment'),
        (r'/\*.*?\*/', 'multiline_comment'),
        (r'\b(?:[0-9]+)\b', 'int_const'),
        (r'\b(?:[0-9][a-zA-Z_]\w*)\b', 'invalid_token'),
    ]

    tokens = tokenize(programming_syntax, token_pattern)
    cfg_result = generate_cfg(tokens)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, cfg_result)
    result_text.config(state=tk.DISABLED)

def tokenize(input_string, token_pattern):
    tokens = []

    for pattern, token_type in token_pattern:
        regex = re.compile(pattern)
        matches = regex.finditer(input_string)

        for match in matches:
            tokens.append((match.group(), token_type))

    return tokens

def generate_cfg(tokens):
    nonterminals = set()
    productions = {}

    for token in tokens:
        nonterminal = token[1]
        if nonterminal not in nonterminals:
            nonterminals.add(nonterminal)
            productions[nonterminal] = [token[0]]
        else:
            productions[nonterminal].append(token[0])

    # Generate the CFG
    cfg_result = ""
    for nonterminal in nonterminals:
        cfg_result += f"{nonterminal} -> {' | '.join(productions[nonterminal])}\n"

    return cfg_result

# GUI setup
app = tk.Tk()
app.title("Programming Syntax to CFG Converter")

browse_button = tk.Button(app, text="Browse", command=browse_file)
browse_button.pack(pady=10)

result_text = tk.Text(app, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(pady=10)

app.mainloop()
