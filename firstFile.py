import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Federal Budget Simulator")
        self.master.geometry("800x600")

        self.budget = {}
        self.total_revenue = 0
        self.total_expenses = 0

        self.create_widgets()
        self.create_chart()

    def create_widgets(self):
        tk.Label(self.master, text="Federal Budget Simulator", font=("Arial", 16)).pack(pady=10)

        # Revenue categories
        self.add_category_widget("Property Tax", 5000000, "revenue")
        self.add_category_widget("Sales Tax", 3000000, "revenue")

        # Expense categories
        self.add_category_widget("Public Safety", 4000000, "expense")
        self.add_category_widget("Infrastructure", 2500000, "expense")
        self.add_category_widget("Parks and Recreation", 1000000, "expense")

        tk.Button(self.master, text="Calculate", command=self.calculate_budget).pack(pady=10)

    def add_category_widget(self, name, amount, category_type):
        frame = tk.Frame(self.master)
        frame.pack(fill="x", padx=10, pady=5)
        tk.Label(frame, text=f"{name}:").pack(side="left")
        entry = tk.Entry(frame)
        entry.insert(0, str(amount))
        entry.pack(side="right")
        self.budget[name] = {"amount": amount, "type": category_type, "entry": entry}
        if category_type == "revenue":
            self.total_revenue += amount
        elif category_type == "expense":
            self.total_expenses += amount

    def create_chart(self):
        self.figure, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(pady=20, expand=True, fill=tk.BOTH)
        self.update_chart()

    def update_chart(self):
        self.ax1.clear()
        self.ax2.clear()
        
        revenue_data = {name: details["amount"] for name, details in self.budget.items() if details["type"] == "revenue"}
        expense_data = {name: details["amount"] for name, details in self.budget.items() if details["type"] == "expense"}

        # Revenue pie chart
        self.ax1.pie(revenue_data.values(), labels=revenue_data.keys(), autopct='%1.1f%%', startangle=90)
        self.ax1.set_title("Revenue Breakdown")

        # Expense pie chart
        self.ax2.pie(expense_data.values(), labels=expense_data.keys(), autopct='%1.1f%%', startangle=90)
        self.ax2.set_title("Expense Breakdown")

        self.figure.tight_layout()
        self.canvas.draw()

    def calculate_budget(self):
        self.total_revenue = 0
        self.total_expenses = 0
        for name, details in self.budget.items():
            try:
                new_amount = float(details["entry"].get())
                self.budget[name]["amount"] = new_amount
                if details["type"] == "revenue":
                    self.total_revenue += new_amount
                elif details["type"] == "expense":
                    self.total_expenses += new_amount
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for {name}")
                return

        balance = self.total_revenue - self.total_expenses
        message = f"Total Revenue: ${self.total_revenue:.2f}\n"
        message += f"Total Expenses: ${self.total_expenses:.2f}\n"
        message += f"Balance: ${balance:.2f}"

        if abs(balance) <= 0.01 * (self.total_revenue + self.total_expenses) / 2:
            messagebox.showinfo("Success", "Congratulations! You've achieved fiscal sustainability.\n\n" + message)
        else:
            messagebox.showwarning("Budget Imbalance", message)

        self.update_chart()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetSimulator(root)
    root.mainloop()