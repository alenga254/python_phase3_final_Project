# python_phase3_final_Project

# Expense Tracker CLI

A simple command-line interface (CLI) application for tracking expenses. The application allows users to add and manage expenses, categorize them, generate reports, and filter expenses based on users or categories.

## Features
- Add users and categories
- Record expenses with user and category associations
- List all users, categories, and expenses
- Filter expenses by user or category
- Update and delete expenses
- Generate a monthly expense report

## Installation

### Prerequisites
Ensure you have Python installed on your system. You also need to install the required dependencies.

### Setting Up the Database
Run the following command to create and seed the database with test data:

```bash
python seed.py
```

## Usage
Run the CLI application using:

```bash
python cli.py
```

### Available Commands
Upon running `cli.py`, you'll see the following options:

```
Expense Tracker CLI
1. Add User
2. List Users
3. Add Category
4. List Categories
5. Add Expense
6. List Expenses
7. Filter Expenses
8. Update Expense
9. Delete Expense
10. Generate Monthly Report
0. Exit
```

### Filtering Expenses
- Filter expenses by user or category
- Example: To filter by category, choose option `7`, then enter a category ID

### Generating Reports
- Select option `10` to generate a monthly report
- Enter the year and month when prompted
- The report displays total expenses and a breakdown by category and user

## Database Schema
The application uses an SQLite database with the following tables:

### Users Table
| ID  | Name | Email           |
| --- | ---- | -------------- |
| 1   | John | john@email.com |

### Categories Table
| ID  | Name         |
| --- | ----------- |
| 1   | Food       |

### Expenses Table
| ID  | Amount | Timestamp           | User ID | Category ID |
| --- | ------ | ------------------ | ------- | ---------- |
| 1   | 2500   | 2025-03-10 14:00:00 | 1       | 2          |

## Dependencies
This project uses:
- `SQLAlchemy` for database management
- `Faker` for generating test data


To install missing dependencies:

```bash
pip install sqlalchemy faker 
```

## License
This project is licensed under the MIT License.

