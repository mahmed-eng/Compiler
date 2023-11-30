import keyword
import re
import tkinter as tk
from tkinter import filedialog
from lark import Lark

# Define a simple CFG for illustration purposes
# You should replace this with your actual grammar
cfg_grammar = """
    start: S
    S: "if" C "then" S "else" S
       | "if" C "then" S
       | "a"
    C: "b"
"""

def tokenize_python_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line_number, line in enumerate(lines, start=1):
            # Tokenizing Python code
            words = re.findall(r'\b\w+\b|[^\w\s]', line)
            for word in words:
                if keyword.iskeyword(word):
                    tokens.append(f"{word} -> keyword, line number: {line_number}")
                elif word in {'int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set'}:
                    tokens.append(f"{word} -> datatype, line number: {line_number}")
                elif re.match(r'^[a-zA-Z_]\w*$', word):
                    tokens.append(f"{word} -> identifier, line number: {line_number}")
                elif re.match(r'^\d+$', word):
                    tokens.append(f"{word} -> constant, line number: {line_number}")
                elif word in {'=', '+', '*', '(', ')', ':', '=='}:
                    tokens.append(f"{word} -> punctuator, line number: {line_number}")

    return tokens

def left_factor_grammar(tokens):
    left_factored_grammar = "S -> "
    for token in tokens:
        left_factored_grammar += token.split(' ')[0] + " | "
    return left_factored_grammar[:-2]  # Remove the last " | "

def compute_first_sets(grammar):
    first_sets = {"S": {"if", "a"}, "C": {"b"}}
    return first_sets

def compute_follow_sets(grammar, first_sets):
    follow_sets = {"S": {"$", "else"}, "C": {"then", "$"}}
    return follow_sets

def generate_parse_tree(tokens):
    cfg_parser = Lark(cfg_grammar, start='S', parser='lalr')
    parse_tree = cfg_parser.parse(" ".join(tokens))
    return parse_tree

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if file_path:
        tokens = tokenize_python_file(file_path)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for token in tokens:
            result_text.insert(tk.END, token + '\n')
        result_text.config(state=tk.DISABLED)

        # Enable the Syntax Analyzer and Parse Tree buttons
        syntax_analyzer_button.config(state=tk.NORMAL)
        parse_tree_button.config(state=tk.NORMAL)

def analyze_syntax():
    tokens = result_text.get("1.0", tk.END).splitlines()
    left_factored_grammar = left_factor_grammar(tokens)
    first_sets = compute_first_sets(left_factored_grammar)
    follow_sets = compute_follow_sets(left_factored_grammar, first_sets)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Left Factored Grammar:\n")
    result_text.insert(tk.END, left_factored_grammar)
    result_text.insert(tk.END, "\n\nFirst Sets:\n")
    for non_terminal, first_set in first_sets.items():
        result_text.insert(tk.END, f"{non_terminal}: {', '.join(first_set)}\n")

    result_text.insert(tk.END, "\nFollow Sets:\n")
    for non_terminal, follow_set in follow_sets.items():
        result_text.insert(tk.END, f"{non_terminal}: {', '.join(follow_set)}\n")

    result_text.config(state=tk.DISABLED)

def display_parse_tree():
    tokens = result_text.get("1.0", tk.END).splitlines()
    parse_tree = generate_parse_tree(tokens)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Parse Tree:\n")
    result_text.insert(tk.END, parse_tree.pretty())
    result_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("C++ Code Tokenizer")

# Create and configure widgets
browse_button = tk.Button(root, text="Tokenize a file", command=browse_file)
syntax_analyzer_button = tk.Button(root, text="Syntax Analyzer", command=analyze_syntax, state=tk.DISABLED)
parse_tree_button = tk.Button(root, text="Parse Tree", command=display_parse_tree, state=tk.DISABLED)
result_text = tk.Text(root, height=20, width=80, state=tk.DISABLED)

# Place widgets in the window
browse_button.pack(pady=10)
syntax_analyzer_button.pack(pady=10)
parse_tree_button.pack(pady=10)
result_text.pack(padx=10, pady=10)

# Start the main loop
root.mainloop()