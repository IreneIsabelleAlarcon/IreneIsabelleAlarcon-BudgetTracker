import flet as ft

# Initialize data
data = {
    "income": [],
    "expenses": [],
    "total_income": 0,
    "total_expenses": 0,
    "budget": 0,
}

# Function to update totals
def update_totals():
    data["total_income"] = sum(item["amount"] for item in data["income"])
    data["total_expenses"] = sum(item["amount"] for item in data["expenses"])
    data["remaining_budget"] = data["total_income"] - data["total_expenses"]

def main(page: ft.Page):
    page.title = "Excel-style Budget Tracker"
    page.scroll = "auto"

    # Create Excel-style table
    income_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Income Source")),
            ft.DataColumn(ft.Text("Amount")),
        ],
        rows=[]
    )

    expense_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Expense Category")),
            ft.DataColumn(ft.Text("Amount")),
        ],
        rows=[]
    )

    # Text to display totals
    total_income_text = ft.Text(f"Total Income: ₱0", size=16, color="green")
    total_expense_text = ft.Text(f"Total Expenses: ₱0", size=16, color="red")
    remaining_budget_text = ft.Text(f"Remaining Budget: ₱0", size=20, color="blue")

    # Update table display
    def update_table():
        income_table.rows.clear()
        for item in data["income"]:
            income_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["source"])),
                        ft.DataCell(ft.Text(f"₱{item['amount']}")),
                    ]
                )
            )

        expense_table.rows.clear()
        for item in data["expenses"]:
            expense_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["category"])),
                        ft.DataCell(ft.Text("₱{item['amount']}")),
                    ]
                )
            )

        total_income_text.value = "Total Income: ₱{data['total_income']}"
        total_expense_text.value = f"Total Expenses: ₱{data['total_expenses']}"
        remaining_budget_text.value = f"Remaining Budget: ₱{data['total_income'] - data['total_expenses']}"

        page.update()

    # Function to add income
    def add_income(e):
        try:
            source = income_source.value
            amount = float(income_amount.value)
            data["income"].append({"source": source, "amount": amount})
            update_totals()
            update_table()
            income_source.value = ""
            income_amount.value = ""
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid income amount!"), open=True)
            page.update()

    # Function to add expense
    def add_expense(e):
        try:
            category = expense_category.value
            amount = float(expense_amount.value)
            data["expenses"].append({"category": category, "amount": amount})
            update_totals()
            update_table()
            expense_category.value = ""
            expense_amount.value = ""
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid expense amount!"), open=True)
            page.update()

    # UI Components
    income_source = ft.TextField(label="Income Source")
    income_amount = ft.TextField(label="Amount (₱)", keyboard_type="number")
    expense_category = ft.TextField(label="Expense Category")
    expense_amount = ft.TextField(label="Amount (₱)", keyboard_type="number")

    add_income_button = ft.ElevatedButton("Add Income", on_click=add_income)
    add_expense_button = ft.ElevatedButton("Add Expense", on_click=add_expense)

    # Layout
    page.add(
        ft.Text("Excel-like Budget Tracker", size=24, weight="bold"),
        ft.Divider(),
        ft.Text("Add Income Entry", size=18),
        income_source,
        income_amount,
        add_income_button,
        income_table,
        ft.Divider(),
        ft.Text("Add Expense Entry", size=18),
        expense_category,
        expense_amount,
        add_expense_button,
        expense_table,
        ft.Divider(),
        total_income_text,
        total_expense_text,
        remaining_budget_text,
    )

    # Initial Update
    update_totals()
    update_table()

if __name__ == "_main_":
    ft.run(main)