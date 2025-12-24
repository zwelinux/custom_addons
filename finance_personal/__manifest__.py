{
    "name": "Personal Finance Manager",
    "summary": "Income, Expense, Budgets, Savings, Debts, Investments (Dividends)",
    "version": "17.0.1.0.0",
    "category": "Productivity",
    "license": "LGPL-3",
    "author": "You",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/category_views.xml",
        "views/wallet_views.xml",
        "views/income_views.xml",
        "views/expense_views.xml",
        "views/saving_goal_views.xml",
        "views/debt_views.xml",
        "views/investment_views.xml",
        "views/dashboard_views.xml",
        "views/menu.xml",              # ← keep this LAST
    ],
    "application": True,
}
