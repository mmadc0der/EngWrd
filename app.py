import tkinter as tk
from tkinter import messagebox, ttk
import asyncio
from threading import Thread
from translator import translate
from storager import WordStorager

def resize_window(window, new_width, new_height):
    # Get current position
    x_pos = window.winfo_x()
    y_pos = window.winfo_y() - 37 # with of the OS window top panel value for debian 12
    
    # Set new geometry while keeping current position
    window.geometry(f"{new_width}x{new_height}+{x_pos}+{y_pos}")

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
        start_button.grid(row=1, column=0, padx=120, pady=5, sticky="we")

        statistics_button = tk.Button(frame, text="Statistics", command=self.show_statistics)
        statistics_button.grid(row=2, column=0, padx=120, pady=5, sticky="we")

        add_word_button = tk.Button(frame, text="Add Word", command=self.add_word)
        add_word_button.grid(row=3, column=0, padx=120, pady=5, sticky="we")

        remove_word_button = tk.Button(frame, text="Remove Word", command=self.remove_word)
        remove_word_button.grid(row=4, column=0, padx=120, pady=5, sticky="we")

        settings_button = tk.Button(frame, text="Settings", command=self.show_settings)
        settings_button.grid(row=5, column=0, padx=120, pady=5, sticky="we")

    def start_training(self):
        # Placeholder for the start training functionality
        messagebox.showinfo("Start", "Start training session")

    # -- Show Statistics
    def show_statistics(self):
        # Placeholder for the statistics functionality
        print(self.word_storager.get_stats())

    # -- Remove Word --
    def remove_word(self):
        # Create a new floating window for deleteon a word
        delete_word_window = tk.Toplevel(self.root)
        delete_word_window.title("Delete Word")
        delete_word_window.geometry("400x110")

        # Entry for the word
        word_label = tk.Label(delete_word_window, text="Enter a word in any language:")
        word_label.pack(pady=5)

        word_entry = tk.Entry(delete_word_window, width=40)
        word_entry.pack(pady=5)

        # Translate button
        translate_button = tk.Button(delete_word_window, text="Delete", command=lambda: self.remove_confirm(word_entry, delete_word_window), width=40)
        translate_button.pack(pady=5)

    def remove_confirm(self, word_entry, delete_word_window):
        word_to_delete = word_entry.get().strip()

        if word_to_delete:
            self.word_storager.delete(word_to_delete)
            delete_word_window.destroy()
            messagebox.showinfo("Success", "Word deleted successfully.")
        else:
            messagebox.showwarning("Error", "Word deleteon failed.")

    # -- Show Settings --
    def show_settings(self):
        # Placeholder for the settings functionality
        messagebox.showinfo("Settings", "Show settings")

    # -- Add Word --
    def add_word(self):
        # Create a new floating window for adding a word
        add_word_window = tk.Toplevel(self.root)
        add_word_window.title("Add Word")
        add_word_window.geometry("400x110")

        # Entry for the word
        word_label = tk.Label(add_word_window, text="Enter a word in any language:")
        word_label.pack(pady=5)

        word_entry = tk.Entry(add_word_window, width=40)
        word_entry.pack(pady=5)

        # Translate button
        translate_button = tk.Button(add_word_window, text="Translate", command=lambda: self.translate_word(word_entry, add_word_window), width=40)
        translate_button.pack(pady=5)

        # Result labels
        self.translated_label = tk.Label(add_word_window, text="", wraplength=350)
        #self.translated_label.pack(padx=10, pady=10)

        self.meaning_label = tk.Label(add_word_window, text="", wraplength=350)
        #self.meaning_label.pack(padx=10, pady=10)

        self.mistakes_label = tk.Label(add_word_window, text="", wraplength=350)
        #self.mistakes_label.pack(padx=10, pady=10)

        # Confirm and Change buttons
        self.button_frame = tk.Frame(add_word_window)
        self.confirm_button = tk.Button(self.button_frame, text="Confirm", command=lambda: self.confirm_word(add_word_window, word_entry), width=18)
        self.change_button = tk.Button(self.button_frame, text="Change", command=lambda: self.change_translation(add_word_window, word_label, word_entry, translate_button), width=18)
        self.confirm_button.grid(row=0, column=1, pady=5)
        self.change_button.grid(row=0, column=0, pady=5)
        self.confirm_button.config(state=tk.DISABLED)
        self.change_button.config(state=tk.DISABLED)

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
        self.button_frame.pack_forget()
        self.translated_label.pack(padx=10, pady=5)
        self.button_frame.pack(pady=5)
        resize_window(add_word_window, 400, 190)

    def run_translate(self, word, add_word_window):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(translate(word))
            loop.close()
            add_word_window.after(0, self.update_translation_result, result, add_word_window)
        except Exception as e:
            add_word_window.after(0, self.show_translation_error, str(e))
        
    def show_translation_error(self, error_message):
        self.translated_label.config(text=f"Error: {error_message}")
        self.meaning_label.config(text="")
        self.mistakes_label.config(text="")
        self.confirm_button.config(state=tk.DISABLED)

    def update_translation_result(self, result, add_word_window):
        if 'error' in result:
            self.show_translation_error(result['error'])
        else:
            self.button_frame.pack_forget()
            self.translated_label.config(text=f"Translated Word: {result['translated_word']}")
            if result['meaning']:
                self.meaning_label.config(text=f"Meaning: {result['meaning']}")
                self.meaning_label.pack(padx=10, pady=5)
            else:
                self.meaning_label.config(text="")
            if result['possible_mistakes']:
                self.mistakes_label.config(text=f"Did you mean: {result['possible_mistakes']}?")
                self.mistakes_label.pack(padx=10, pady=5)
            else:
                self.mistakes_label.config(text="")
            self.confirm_button.config(state=tk.NORMAL)
            self.change_button.config(state=tk.NORMAL)
            self.button_frame.pack()
            add_word_window.update_idletasks()
            resize_window(add_word_window,
                400, 190 \
                + ((self.meaning_label.winfo_height() + 5) if self.meaning_label.winfo_height() > 1 else 0) \
                + ((self.mistakes_label.winfo_height() + 5) if self.mistakes_label.winfo_height() > 1 else 0)
            )

    def change_translation(self, add_word_window, word_label, word_entry, translate_button):
        self.meaning_label.pack_forget()
        self.mistakes_label.pack_forget()
        self.button_frame.pack_forget()
        word_label.config(text='Enter word in English:')
        self.translated_label.config(text='Enter word translation:')
        translate_button.pack_forget()
        resize_window(add_word_window, 400, 190)
        translate_entry = tk.Entry(add_word_window, width=40)
        translate_entry.pack(pady=5)
        confirm_button = tk.Button(add_word_window, text="Confirm", command=lambda: self.confirm_word(add_word_window, word_entry, translate_entry), width=40)
        confirm_button.pack(pady=5)

    def confirm_word(self, add_word_window, word_entry, translate_entry = None):
        translated_word = self.translated_label.cget("text").split(": ")[1] if not translate_entry else translate_entry.get().strip()
        meaning = self.meaning_label.cget("text").split(": ")[1] if self.meaning_label.cget("text") else None
        original_word = word_entry.get().strip()

        if translated_word and original_word:
            self.word_storager.store(original_word, translated_word, meaning)
            add_word_window.destroy()
            messagebox.showinfo("Success", "Word added successfully.")
        else:
            messagebox.showwarning("Error", "Word addition failed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()