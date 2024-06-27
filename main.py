import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

path: str = "anki_notes.txt"

class AnkiNoteSaver:
    def __init__(self, root):
        self.root = root
        self.notes = []

        self.root.title("Anki Note Saver")

        tk.Label(root, text="Field 1:").grid(row=0, column=0, padx=10, pady=10)
        self.entry1 = tk.Entry(root, width=40)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Field 2:").grid(row=1, column=0, padx=10, pady=10)
        self.entry2 = tk.Entry(root, width=40)
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        add_button = tk.Button(root, text="Add Note", command=self.add_note)
        add_button.grid(row=2, column=0, pady=20)

        save_button = tk.Button(root, text="Save Notes", command=self.save_notes)
        save_button.grid(row=2, column=1, pady=20)

        # Set up the Treeview
        self.tree = ttk.Treeview(root, columns=('Field1', 'Field2'), show='headings')
        self.tree.heading('Field1', text='Field 1')
        self.tree.heading('Field2', text='Field 2')
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.tree.bind('<Double-1>', self.edit_note)

        # Make the treeview resize with the window
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Load existing notes
        self.load_notes()

    def add_note(self):
        field1 = self.entry1.get()
        field2 = self.entry2.get()

        if not field1 or not field2:
            messagebox.showwarning("Input Error", "Both fields must be filled out.")
            return

        self.notes.append((field1, field2))
        self.tree.insert('', 'end', values=(field1, field2))

        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)

    def edit_note(self, event):
        selected_item = self.tree.selection()[0]
        self.selected_index = self.tree.index(selected_item)
        values = self.tree.item(selected_item, 'values')

        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, values[0])
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, values[1])

        self.tree.delete(selected_item)
        self.notes.pop(self.selected_index)

    def save_notes(self):
        if not self.notes:
            messagebox.showwarning("Save Error", "No notes to save.")
            return

        with open(path, "w") as file:
            for note in self.notes:
                file.write(f"{note[0]}\t{note[1]}\n")

        messagebox.showinfo("Success", "All notes saved successfully.")
        self.notes.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def load_notes(self):
        if os.path.exists(path):
            with open(path, "r") as file:
                for line in file:
                    field1, field2 = line.strip().split('\t')
                    self.notes.append((field1, field2))
                    self.tree.insert('', 'end', values=(field1, field2))


# Create the main window and run the application
root = tk.Tk()
app = AnkiNoteSaver(root)


# Ensure the update button also resizes with the window
root.grid_rowconfigure(4, weight=0)

root.mainloop()
