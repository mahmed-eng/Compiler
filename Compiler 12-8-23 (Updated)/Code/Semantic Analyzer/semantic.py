import re
import tkinter as tk
from tkinter import filedialog

class Token:
    def __init__(self, token_class, value, line_number):
        self.token_class = token_class
        self.value = value
        self.line_number = line_number

class Attribute:
    def __init__(self, attribute_type, value):
        self.attribute_type = attribute_type
        self.value = value

def tokenize_line(line, line_number):
    tokens = []
    token_patterns = [
        # ... (same token patterns as before)
    ]

    for pattern, token_class in token_patterns:
        matches = re.finditer(pattern, line)
        for match in matches:
            value = match.group(0)
            tokens.append(Token(token_class, value, line_number))

    return tokens

def tokenize_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line_tokens = tokenize_line(line, line_number)
            tokens.extend(line_tokens)

    return tokens

def generate_cfg_rules(file_path):
    cfg_rules = ""
    with open(file_path, 'r') as file:
        in_class_body = False
        for line in file:
            line = line.strip()
            if line.startswith("class"):
                class_name = line.split()[1].split(":")[0]
                cfg_rules += f"\n<{class_name}_definition> -> class {class_name} : <class_body>"
                in_class_body = True
            elif line.startswith("def"):
                method_name = line.split()[1].split("(")[0]
                if in_class_body:
                    cfg_rules += f"\n<{method_name}> -> {method_name} ( <parameters> ) : <method_body>"
            elif line.startswith("@staticmethod def"):
                method_name = line.split()[3].split("(")[0]
                if in_class_body:
                    cfg_rules += f"\n<{method_name}> -> @staticmethod {method_name} ( <parameters> ) : <method_body>"
            elif line.startswith("def __init__"):
                if in_class_body:
                    cfg_rules += f"\n<constructor_definition> -> def __init__ ( self ) : <method_body>"
            elif line.startswith("def __del__"):
                if in_class_body:
                    cfg_rules += f"\n<destructor_definition> -> def __del__ ( self ) : <method_body>"
            elif line.startswith("try"):
                cfg_rules += "\n<try_catch_block> -> try : <statements> except <exception_type> as <exception_var> : <statements> finally : <statements>"
            elif line.startswith("except"):
                exception_type = line.split()[1]
                cfg_rules += f"\n<exception_type> -> {exception_type}"
            elif line.startswith("finally"):
                cfg_rules += "\n<finally_block> -> finally : <statements>"
            elif line.startswith("print"):
                cfg_rules += "\n<print_statement> -> print ( <expression> )"

    return cfg_rules

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

def analyze_semantics():
    file_path = file_path_entry.get()
    tokens = tokenize_file(file_path)

    cfg_rules = generate_cfg_rules(file_path)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, cfg_rules)

# Create the main window
root = tk.Tk()
root.title("Attributed CFG Generation App")

# Create and configure the GUI components
file_path_label = tk.Label(root, text="File Path:")
file_path_label.pack(pady=5)

file_path_entry = tk.Entry(root, width=50)
file_path_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

analyze_button = tk.Button(root, text="Generate Attributed CFG", command=analyze_semantics)
analyze_button.pack(pady=10)

result_text = tk.Text(root, height=20, width=80)
result_text.pack()

# Start the main loop
root.mainloop()
