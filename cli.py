from database import Session
from models.user import User
from models.category import Category
from models.expense import Expense
from datetime import datetime
from sqlalchemy.sql import extract 

def create_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")

    session = Session()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.close()
    print( f"User {name} created successfully!")

def list_users():
    session = Session()
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    session.close()

def create_category():
    name = input("Enter the name of the category: ")
    session = Session()
    category = Category(name=name)
    session.add(category)
    session.commit()
    session.close()
    print(f"Category {name} created successfully!")

def list_categories():
    session = Session()
    categories = session.query(Category).all()
    for category in categories:
        print(f"ID: {category.id}, Name: {category.name}")
    session.close()

def add_expense():
    try:
        amount = int(input("Enter expense amount: "))
        if amount <= 0:
            raise ValueError("Expense amount must be a positive integer.")
    except ValueError:
        print("Invalid input! Please enter a positive whole number.")
        return

    user_id = int(input("Enter user ID: "))
    category_id = int(input("Enter category ID: "))

    session = Session()
    user = session.get(User, user_id)
    category = session.get(Category, category_id)

    if not user or not category:
        print("Invalid user or category ID. Please try again.")
        session.close()
        return

    expense = Expense(amount=amount, user_id=user_id, category_id=category_id, timestamp=datetime.now())
    session.add(expense)
    session.commit()
    session.close()
    print(f"Expense of {amount} added successfully!")


def list_expenses():
    session = Session()
    expenses = session.query(Expense).all()
    for expense in expenses:
        print(f"ID: {expense.id}, Amount: {expense.amount}, User ID: {expense.user_id}, Category ID: {expense.category_id}, Timestamp: {expense.timestamp}")
    session.close()

def filter_expenses():
    print("Filter by:")
    print("1. User")
    print("2. Category")
    choice = input("Enter choice: ")

    session = Session()
    if choice == "1":
        user_id = int(input("Enter user ID: "))
        expenses = session.query(Expense).filter_by(user_id=user_id).all()
    elif choice == "2":
        category_id = int(input("Enter category ID: "))
        expenses = session.query(Expense).filter_by(category_id=category_id).all()
    else:
        print("Invalid choice!")
        return
    
    session.close()
    
    if expenses:
        for expense in expenses:
            print(f"ID: {expense.id}, Amount: {expense.amount}, Date: {expense.timestamp}")
    else:
        print("No expenses found.")

def update_expense():
    expense_id = int(input("Enter the expense ID to update: "))

    session = Session()
    expense = session.query(Expense).get(expense_id)

    if not expense:
        print("Expense not found!")
        return

    print("Leave blank if you don't want to update a field.")
    
    new_amount = input(f"Enter new amount (current: {expense.amount}): ")
    if new_amount:
        expense.amount = int(new_amount)

    new_category_id = input(f"Enter new category ID (current: {expense.category_id}): ")
    if new_category_id:
        category = session.query(Category).get(int(new_category_id))
        if category:
            expense.category_id = int(new_category_id)
        else:
            print("Invalid category ID!")

    new_user_id = input(f"Enter new user ID (current: {expense.user_id}): ")
    if new_user_id:
        user = session.query(User).get(int(new_user_id))
        if user:
            expense.user_id = int(new_user_id)
        else:
            print("Invalid user ID!")

    session.commit()
    session.close()
    print("Expense updated successfully!")

def delete_expense ():
    expense_id = int(input("Enter expense ID: "))

    session = Session()
    expense = session.query(Expense).get(expense_id)

    if expense:
        session.delete(expense)
        session.commit()
        print("Expense deleted successfully!")
    else:
        print("Expense not found!")
    
    session.close()

def generate_monthly_report():
    year = int(input("Enter year (YYYY): "))
    month = int(input("Enter month (MM): "))

    session = Session()
    expenses = session.query(Expense).filter(
        extract('year', Expense.timestamp) == year,   # ✅ Use extract for year
        extract('month', Expense.timestamp) == month
    ).all()
    session.close()

    if not expenses:
        print("No expenses found for the given month.")
        return

    total_amount = sum(expense.amount for expense in expenses)
    print(f"\nMonthly Expense Report for {year}-{month:02d}")
    print(f"Total Expenses: {total_amount:.2f}")

    for expense in expenses:
        print(f"ID: {expense.id}, Amount: {expense.amount}, Category: {expense.category_id}, User: {expense.user_id}, Date: {expense.timestamp}")


def main():
    while True:
        print("\nExpense Tracker CLI")
        print("1. Add User")
        print("2. List Users")
        print("3. Add Category")
        print("4. List Categories")
        print("5. Add Expense")
        print("6. List Expenses")
        print("7. Update Expense")
        print("8. Delete Expense")
        print("9. Generate Monthly Report")
        print("10. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            create_category()
        elif choice == "4":
            list_categories()
        elif choice == "5":
            add_expense()
        elif choice == "6":
            list_expenses()
        elif choice == "7":
            update_expense()
        elif choice == "8":
            delete_expense()
        elif choice == "9":
            generate_monthly_report()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid option! Please choose again.")
       
       

if __name__ == "__main__":
    main()   
