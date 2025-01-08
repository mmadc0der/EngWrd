import tkinter as tk
from tkinter import messagebox
import asyncio
from threading import Thread
from translator import translate
from storager import WordStorager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Russian-English Word Trainer")
        self.word_storager = WordStorager()
        self.create_main_menu()

    def create_main_menu(self):
        # Set the window size
        self.root.geometry("800x480")
        
        # Center the buttons in the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a frame to hold the buttons
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure the frame to center the buttons
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(6, weight=1)

        # Create and place the buttons
        start_button = tk.Button(frame, text="Start", command=self.start_training)
        start_button.grid(row=1, column=0, padx=120, pady=10, sticky="we")

        statistics_button = tk.Button(frame, text="Statistics", command=self.show_statistics)
        statistics_button.grid(row=2, column=0, padx=120, pady=10, sticky="we")

        add_word_button = tk.Button(frame, text="Add Word", command=self.add_word)
        add_word_button.grid(row=3, column=0, padx=120, pady=10, sticky="we")

        remove_word_button = tk.Button(frame, text="Remove Word", command=self.remove_word)
        remove_word_button.grid(row=4, column=0, padx=120, pady=10, sticky="we")

        settings_button = tk.Button(frame, text="Settings", command=self.show_settings)
        settings_button.grid(row=5, column=0, padx=120, pady=10, sticky="we")

    def start_training(self):
        # Placeholder for the start training functionality
        messagebox.showinfo("Start", "Start training session")

    def show_statistics(self):
        # Placeholder for the statistics functionality
        messagebox.showinfo("Statistics", "Show statistics")

    def remove_word(self):
        # Placeholder for the remove word functionality
        messagebox.showinfo("Remove Word", "Remove a word")

    def show_settings(self):
        # Placeholder for the settings functionality
        messagebox.showinfo("Settings", "Show settings")

    def add_word(self):
        # Create a new floating window for adding a word
        add_word_window = tk.Toplevel(self.root)
        add_word_window.title("Add Word")
        add_word_window.geometry("400x300")

        # Entry for the word
        word_label = tk.Label(add_word_window, text="Enter a word in any language:")
        word_label.pack(pady=10)

        word_entry = tk.Entry(add_word_window, width=50)
        word_entry.pack(pady=10)

        # Translate button
        translate_button = tk.Button(add_word_window, text="Translate", command=lambda: self.translate_word(word_entry, add_word_window))
        translate_button.pack(pady=10)

        # Result labels
        self.translated_label = tk.Label(add_word_window, text="")
        self.translated_label.pack(pady=10)

        self.meaning_label = tk.Label(add_word_window, text="")
        self.meaning_label.pack(pady=10)

        self.mistakes_label = tk.Label(add_word_window, text="")
        self.mistakes_label.pack(pady=10)

        # Confirm button
        self.confirm_button = tk.Button(add_word_window, text="Confirm", command=lambda: self.confirm_word(add_word_window))
        self.confirm_button.pack(pady=10)
        self.confirm_button.config(state=tk.DISABLED)

    def translate_word(self, word_entry, add_word_window):
        word = word_entry.get().strip()
        if word:
            self.translated_label.config(text="Translating...")
            self.meaning_label.config(text="")
            self.mistakes_label.config(text="")
            self.confirm_button.config(state=tk.DISABLED)
            thread = Thread(target=self.run_translate, args=(word, add_word_window))
            thread.start()
        else:
            self.translated_label.config(text="Please enter a word.")

    def run_translate(self, word, add_word_window):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translate(word))
        loop.close()

        add_word_window.after(0, self.update_translation_result, result)

    def update_translation_result(self, result):
        self.translated_label.config(text=f"Translated Word: {result['translated_word']}")
        
        if result['meaning']:
            self.meaning_label.config(text=f"Meaning: {result['meaning']}")
        else:
            self.meaning_label.config(text="")

        if result['possible_mistakes']:
            self.mistakes_label.config(text=f"Did you mean: {', '.join(result['possible_mistakes'])}?")
        else:
            self.mistakes_label.config(text="")

        self.confirm_button.config(state=tk.NORMAL)

    def confirm_word(self, add_word_window):
        translated_word = self.translated_label.cget("text").split(": ")[1]
        meaning = self.meaning_label.cget("text").split(": ")[1] if self.meaning_label.cget("text") else None
        original_word = self.translated_label.cget("text").split(": ")[0].split(" ")[-1]

        if translated_word and original_word:
            self.word_storager.store(original_word, translated_word, meaning)
            add_word_window.destroy()
            messagebox.showinfo("Success", "Word added successfully.")
        else:
            messagebox.showwarning("Error", "Translation failed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()