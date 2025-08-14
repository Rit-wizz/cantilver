import tkinter as tk
from tkinter import messagebox, ttk

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x400")

        self.expenses = []  # List of dictionaries

        self.setup_ui()

    def setup_ui(self):
        # Labels
        tk.Label(self.root, text="Description:", fg="blue").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.root, text="Amount (₹):", fg="blue").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(self.root, text="Category:", fg="blue").grid(row=2, column=0, padx=5, pady=5, sticky="e")

        # Entry fields
        self.desc_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()

        tk.Entry(self.root, textvariable=self.desc_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.amount_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.category_var, width=30).grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Expense", width=15, command=self.add_expense).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Reset", width=15, command=self.reset_expenses).grid(row=3, column=1, padx=5, pady=5)

        # Table for expenses
        self.tree = ttk.Treeview(self.root, columns=("Description", "Amount", "Category"), show="headings")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount (₹)")
        self.tree.heading("Category", text="Category")
        self.tree.column("Description", width=150)
        self.tree.column("Amount", width=80, anchor="center")
        self.tree.column("Category", width=100, anchor="center")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Total Label
        self.total_label = tk.Label(self.root, text="Total: ₹0", font=("Arial", 12, "bold"), fg="green")
        self.total_label.grid(row=5, column=0, columnspan=2, pady=10)

    def add_expense(self):
        desc = self.desc_var.get().strip()
        amount = self.amount_var.get().strip()
        category = self.category_var.get().strip()

        if not desc or not amount or not category:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number.")
            return

        self.expenses.append({"Description": desc, "Amount": amount, "Category": category})
        self.tree.insert("", tk.END, values=(desc, f"{amount:.2f}", category))

        self.update_total()
        self.clear_fields()

    def clear_fields(self):
        self.desc_var.set("")
        self.amount_var.set("")
        self.category_var.set("")

    def reset_expenses(self):
        confirm = messagebox.askyesno("Reset", "Clear all expenses?")
        if confirm:
            self.expenses.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.update_total()

    def update_total(self):
        total = sum(exp["Amount"] for exp in self.expenses)
        self.total_label.config(text=f"Total: ₹{total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()