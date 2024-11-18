import flet as ft
from datetime import datetime

from flet_core.colors import BLUE_500

# Global Variables
income = []
expenses = []
total_balance = 0


def main(page: ft.Page):
    global income, expenses, total_balance

    # Set the blue background and black text
    page.bgcolor = ft.colors. BLUE_900  # blue background
    page.theme_mode = ft.ThemeMode.DARK  # Dark theme for black text
    page.title = "Budget Tracker"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    # Create a scrollable container (ListView)
    page.add(ft.ListView(
        controls=[
            # Title and introductory text
            ft.Text("Budget Tracker", style=ft.TextStyle(color=ft.colors.WHITE, size=30, weight=ft.FontWeight.BOLD)),
            ft.Text("Enter income and expenses to track your budget.", color=ft.colors.WHITE, size=20),

            # Income Section
            ft.Text("Enter Income", style=ft.TextStyle(color=ft.colors.WHITE, size=20)),
            ft.Row([
                ft.Column([ft.Text("Name:", color=ft.colors.WHITE)]),
                ft.Column([ft.Text("Amount:", color=ft.colors.WHITE)])
            ]),
            income_name_field := ft.TextField(hint_text="Enter income name", autofocus=True),
            income_amount_field := ft.TextField(hint_text="Enter income amount"),
            add_income_button := ft.ElevatedButton(text="Add Income",
                                                   on_click=lambda e: add_income(income_name_field, income_amount_field,
                                                                                 display_list, summary_text)),

            # Expenses Section
            ft.Text("Enter Expenses", style=ft.TextStyle(color=ft.colors.WHITE, size=20)),
            ft.Row([
                ft.Column([ft.Text("Name:", color=ft.colors.WHITE)]),
                ft.Column([ft.Text("Amount:", color=ft.colors.WHITE)])
            ]),
            expense_name_field := ft.TextField(hint_text="Enter expense name"),
            expense_amount_field := ft.TextField(hint_text="Enter expense amount"),
            add_expense_button := ft.ElevatedButton(text="Add Expense",
                                                    on_click=lambda e: add_expense(expense_name_field,
                                                                                   expense_amount_field, display_list,
                                                                                   summary_text)),

            # Total Balance Section
            total_balance_button := ft.ElevatedButton(text="Calculate Total Balance",
                                                      on_click=lambda e: update_summary(summary_text)),

            display_list := ft.ListView(expand=1, spacing=10),
            summary_text := ft.Text(size=18, weight=ft.FontWeight.BOLD),
        ]
    ))

    # Update Display on Load
    update_display(display_list)
    update_summary(summary_text)


def add_income(income_name_field, income_amount_field, display_list, summary_text):
    global income
    name = income_name_field.value
    amount = income_amount_field.value
    if amount and amount.isnumeric():
        income.append({"name": name, "amount": int(amount), "type": "Income", "date": get_current_date()})
        income_name_field.value = ""
        income_amount_field.value = ""
        update_display(display_list)
        update_summary(summary_text)
    elif amount:
        ft.SnackBar(ft.Text("Invalid income amount")).open()


def add_expense(expense_name_field, expense_amount_field, display_list, summary_text):
    global expenses
    name = expense_name_field.value
    amount = expense_amount_field.value
    if amount and amount.isnumeric():
        expenses.append({"name": name, "amount": int(amount), "type": "Expense", "date": get_current_date()})
        expense_name_field.value = ""
        expense_amount_field.value = ""
        update_display(display_list)
        update_summary(summary_text)
    elif amount:
        ft.SnackBar(ft.Text("Invalid expense amount")).open()


def update_display(display_list):
    global income, expenses, total_balance
    display_list.controls.clear()

    # Display Income entries
    for item in income:
        row = ft.Row([
            ft.Column([ft.Text(f"{item['type']}: {item['name']} on {item['date']}", size=16, color=ft.colors.BLACK)]),
            ft.Column([ft.Text(f"${item['amount']}", size=16, color=ft.colors.BLACK)]),
        ])
        display_list.controls.append(row)

    # Display Expenses entries
    for item in expenses:
        row = ft.Row([
            ft.Column([ft.Text(f"{item['type']}: {item['name']} on {item['date']}", size=16, color=ft.colors.BLACK)]),
            ft.Column([ft.Text(f"${item['amount']}", size=16, color=ft.colors.BLACK)]),
        ])
        display_list.controls.append(row)

    display_list.update()


def update_summary(summary_text):
    global income, expenses, total_balance
    total_income = sum(item['amount'] for item in income)
    total_expenses = sum(item['amount'] for item in expenses)
    total_balance = total_income - total_expenses

    # Add the current date to the summary
    current_date = get_current_date()
    summary_text.value = f"Summary ({current_date}):\nIncome: ${total_income}, Expenses: ${total_expenses}, Remaining Balance: ${total_balance}"
    summary_text.update()


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Run the app
ft.app(target=main)
ft.app(target=main, view=ft.WEB_BROWSER())