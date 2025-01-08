import asyncio
import tkinter as tk
from translator import translate  # Import your translate function

# Main application window setup
root = tk.Tk()
root.title("English Words Learning App")
root.geometry("1200x720")

# Main menu button to add a new word
add_word_button = tk.Button(root, text="Add Word", command=lambda: print('pressed'))

button_frame = tk.Frame(root)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

tk.Button(button_frame, text="Add Word", command=lambda: print('pressed')).grid(row=0, column=1, sticky=tk.W+tk.E)
tk.Button(button_frame, text="Add Word", command=lambda: print('pressed')).grid(row=1, column=1, sticky=tk.W+tk.E)
tk.Button(button_frame, text="Add Word", command=lambda: print('pressed')).grid(row=2, column=1, sticky=tk.W+tk.E)
button_frame.pack(fill=tk.X, pady=200)

root.mainloop()
