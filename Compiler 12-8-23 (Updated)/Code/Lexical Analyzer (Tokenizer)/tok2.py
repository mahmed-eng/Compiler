import re
import tkinter as tk
from tkinter import filedialog

class Token:
    def __init__(self, token_class, value, line_number):
        self.token_class = token_class
        self.value = value
        self.line_number = line_number

def is_valid_variable_name(name):
    return not name[0].isdigit()

def tokenize_line(line, line_number):
    tokens = []
    token_patterns = [
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

    for pattern, token_class in token_patterns:
        matches = re.finditer(pattern, line)
        for match in matches:
            value = match.group(0)
            if token_class == 'invalid_token' and not is_valid_variable_name(value):
                tokens.append(Token(token_class, value, line_number))
            elif token_class != 'invalid_token':
                tokens.append(Token(token_class, value, line_number))

    return tokens

def tokenize_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line_tokens = tokenize_line(line, line_number)
            tokens.extend(line_tokens)

    return tokens

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

def display_tokens():
    file_path = file_path_entry.get()
    tokens = tokenize_file(file_path)
    
    result_text.delete(1.0, tk.END)
    for token in tokens:
        result_text.insert(tk.END, f"Class Part: {token.token_class}, Value Part: {token.value}, Line Number: {token.line_number}\n")

    # Save tokens to a file
    save_tokens_to_file(tokens, "generated_tokens.txt")

def save_tokens_to_file(tokens, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for token in tokens:
            file.write(f"{token.token_class} {token.value} {token.line_number}\n")

def syntax_analyzer():
    # Save tokens to a file before calling syntax.py
    tokens = tokenize_file("generated_tokens.txt")
    save_tokens_to_file(tokens, "generated_tokens_for_syntax.txt")

    # Call syntax.py with the full path
    import subprocess
    subprocess.run(["python", r"C:\Users\Azharuddin\Downloads\Python\Lexical_Analyzer-Parser_Implemented-in-Python-master\Syntax\syntax.py"])

def semantic_analyzer():
    # Call semantic.py with the full path
    import subprocess
    subprocess.run(["python", r"C:\Users\Azharuddin\Downloads\Python\Lexical_Analyzer-Parser_Implemented-in-Python-master\Syntax\semantic.py"])

# Create the main window
root = tk.Tk()
root.title("Tokenization App")

# Create and configure the GUI components
file_path_label = tk.Label(root, text="File Path:")
file_path_label.pack(pady=5)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

result_text = tk.Text(root, height=20, width=80)
result_text.pack()

display_tokens_button = tk.Button(root, text="Display Tokens", command=display_tokens)
display_tokens_button.pack(pady=10)

syntax_analyzer_button = tk.Button(root, text="Syntax Analyzer", command=syntax_analyzer)
syntax_analyzer_button.pack(pady=10)

semantic_analyzer_button = tk.Button(root, text="Semantic Analyzer", command=semantic_analyzer)
semantic_analyzer_button.pack(pady=10)

# Start the main loop
root.mainloop()
