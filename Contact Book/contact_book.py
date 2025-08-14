import tkinter as tk
from tkinter import messagebox

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Layout AddressBook")

        self.contacts = {}
        self.selected_contact = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Name", fg="blue").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Label(self.root, text="Phone", fg="blue").grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        self.name_entry = tk.Entry(self.root, textvariable=self.name_var, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.phone_entry = tk.Entry(self.root, textvariable=self.phone_var, width=25)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        self.clear_btn = tk.Button(self.root, text="Clear", width=10, command=self.clear_fields)
        self.clear_btn.grid(row=2, column=0, padx=5, pady=5)

        self.add_btn = tk.Button(self.root, text="Add", width=10, command=self.add_contact)
        self.add_btn.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.update_btn = tk.Button(self.root, text="Update", width=10, command=self.update_contact)
        self.update_btn.grid(row=3, column=0, padx=5, pady=5)

        self.delete_btn = tk.Button(self.root, text="Delete", width=10, command=self.delete_contact)
        self.delete_btn.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.reset_btn = tk.Button(self.root, text="Reset", width=10, command=self.reset_contacts)
        self.reset_btn.grid(row=4, column=0, padx=5, pady=5)

        self.contact_listbox = tk.Listbox(self.root, width=30, height=10)
        self.contact_listbox.grid(row=0, column=2, rowspan=6, padx=10, pady=5)
        self.contact_listbox.bind("<<ListboxSelect>>", self.on_select)

    def refresh_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for name in sorted(self.contacts):
            self.contact_listbox.insert(tk.END, name)

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.selected_contact = None
        self.add_btn.config(state=tk.NORMAL)
        self.contact_listbox.selection_clear(0, tk.END)

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Missing Info", "Please enter both name and phone.")
            return

        if name in self.contacts:
            messagebox.showerror("Exists", "Contact already exists.")
        else:
            self.contacts[name] = phone
            self.refresh_listbox()
            self.clear_fields()

    def update_contact(self):
        if self.selected_contact:
            new_name = self.name_var.get().strip()
            new_phone = self.phone_var.get().strip()

            if not new_name or not new_phone:
                messagebox.showwarning("Missing Info", "Name and phone cannot be empty.")
                return

            if new_name != self.selected_contact and new_name in self.contacts:
                messagebox.showerror("Duplicate", "Another contact with that name exists.")
                return

            del self.contacts[self.selected_contact]
            self.contacts[new_name] = new_phone
            self.refresh_listbox()
            self.clear_fields()

    def delete_contact(self):
        if self.selected_contact:
            confirm = messagebox.askyesno("Confirm Delete", f"Delete contact '{self.selected_contact}'?")
            if confirm:
                del self.contacts[self.selected_contact]
                self.refresh_listbox()
                self.clear_fields()

    def reset_contacts(self):
        confirm = messagebox.askyesno("Reset", "Clear all contacts?")
        if confirm:
            self.contacts = {}
            self.refresh_listbox()
            self.clear_fields()

    def on_select(self, event):
        selected = event.widget.curselection()
        if selected:
            name = event.widget.get(selected[0])
            self.name_var.set(name)
            self.phone_var.set(self.contacts[name])
            self.selected_contact = name
            self.add_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()