# FinSight 💰📊

**FinSight** is a Django-based Personal Finance Analytics Platform designed to help users manage their income, expenses, budgets, and financial insights in one place.

## 🔗 Project Repository

[View FinSight on GitHub](https://github.com/anamikag9641-svg/FinSight)

http://127.0.0.1:8000/accounts/login/

## 📌 About the Project

FinSight allows users to record and manage their financial transactions, create budgets, and analyze their spending through an interactive dashboard.

The project was developed to apply concepts of:

- Django Web Development
- Python
- SQL / SQLite Database Management
- CRUD Operations
- Data Analysis
- Data Visualization
- User Authentication

## ✨ Features

### 🔐 User Authentication
- User registration
- User login and logout
- User-specific financial data

### 💸 Transaction Management
- Add income transactions
- Add expense transactions
- Categorize transactions
- Add descriptions and dates
- View recent transactions
- Delete transactions

### 🎯 Budget Management
- Create monthly budgets
- Set category-specific budgets
- Set overall budgets
- Track budget spending
- View remaining budget
- Visual budget progress indicators
- Budget status:
  - ✓ Within Budget
  - ⚠ Budget Almost Reached
  - 🚨 Over Budget

### 📊 Financial Dashboard
The dashboard provides an overview of:

- Total Income
- Total Expenses
- Current Balance
- Monthly Spending
- Total Budget
- Budget Spent
- Budget Remaining
- Recent Transactions

### 📈 Analytics
FinSight provides financial analytics including:

- Total spending
- Average expense
- Highest expense
- Number of expenses
- Category-wise spending analysis
- Expense distribution charts
- Spending summaries

### 📉 Data Visualization

Interactive charts are created using **Chart.js**, including:

- Expense category doughnut chart
- Monthly spending trend
- Budget vs Actual spending chart

## 🛠️ Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Database
- SQLite
- Django ORM

### Development Tools
- Visual Studio Code
- Git
- GitHub

## 🏗️ Project Structure

```text
FinSight/
│
├── accounts/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── analytics/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── budgets/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── transactions/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── .gitignore
└── README.md
