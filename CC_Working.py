import tkinter as tk
from LexicalAnalyzer import GenerateTokens
from LexicalAnalyzer import LexicalError
from SyntaxAnalyzer import SyntaxAnalyzer

def append_text(widget, text, color):
    widget.config(state=tk.NORMAL)
    widget.insert(tk.END, text, color)
    widget.config(state=tk.DISABLED)

def on_generate_tokens():
    debug_window.config(state=tk.NORMAL)
    debug_window.delete("1.0", tk.END)
    debug_window.config(state=tk.DISABLED)

    code_text = code_area.get("1.0", tk.END).strip()
    try:
        token_list = GenerateTokens.generate(code_text)
        if token_list is not None:
            append_text(debug_window, "[Lexical Error] No Lexical error found. \n", "green")

            try:
                result = SyntaxAnalyzer.Start(token_list)
                if result:
                    append_text(debug_window, "[Syntax Error] No syntax error found. \n", "green")
                else:
                    append_text(debug_window, "[Syntax Error] Syntax error at unspecified line number \n", "red")
            except SyntaxError as e:
                append_text(debug_window, f"[Syntax Error] Syntax error at line number: {e.line}  At Non-Terminal: {e.non_terminal_name}\n", "red")
            except Exception as e:
                append_text(debug_window, f"[Internal Error] {type(e).__name__}: {str(e)}\n", "red")
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