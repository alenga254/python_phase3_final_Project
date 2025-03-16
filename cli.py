from database import Session
from models.user import User
from models.category import Category
from models.expense import Expense
from datetime import datetime
from sqlalchemy.sql import extract 
from sqlalchemy import func

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
    expenses = session.query(Expense).join(User).join(Category).all()

    for expense in expenses:
        print(f"ID: {expense.id}, Amount: {expense.amount}, "
              f"User: {expense.user.name}, Category: {expense.category.name}, "
              f"Timestamp: {expense.timestamp}")

    session.close()


def filter_expenses():
    print("\nFilter by:")
    print("1. User")
    print("2. Category")
    choice = input("Enter choice: ").strip()

    session = Session()

    try:
        if choice == "1":
            user_id = input("Enter user ID: ").strip()
            if not user_id.isdigit():
                print("Invalid user ID! Please enter a valid number.")
                return
            
            expenses = (
                session.query(Expense)
                .join(User)
                .filter(Expense.user_id == int(user_id))
                .all()
            )

        elif choice == "2":
            category_id = input("Enter category ID: ").strip()
            if not category_id.isdigit():
                print("Invalid category ID! Please enter a valid number.")
                return
            
            expenses = (
                session.query(Expense)
                .join(Category)
                .filter(Expense.category_id == int(category_id))
                .all()
            )

        else:
            print("Invalid choice! Please enter 1 or 2.")
            return

        # Check if there are any expenses
        if not expenses:
            print("\nNo expenses found.")
        else:
            print("\nFiltered Expenses:")
            for expense in expenses:
                print(
                    f"ID: {expense.id}, Amount: {expense.amount}, "
                    f"User: {expense.user.name}, Category: {expense.category.name}, "
                    f"Date: {expense.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
                )
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        session.close()

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
    year = input("Enter year (YYYY): ")
    month = input("Enter month (MM): ").zfill(2)  

    session = Session()

    expenses = session.query(Expense).join(User).join(Category).filter(
        func.strftime('%Y', Expense.timestamp) == year,
        func.strftime('%m', Expense.timestamp) == month
    ).all()

    if not expenses:
        print(f"\nNo expenses found for {year}-{month}.")
        return

    total_expense = sum(exp.amount for exp in expenses)

    print(f"\nMonthly Expense Report for {year}-{month}")
    print(f"Total Expenses: {total_expense:.2f}")

    for exp in expenses:
        print(f"ID: {exp.id}, Amount: {exp.amount}, Category: {exp.category.name}, User: {exp.user.name}, Date: {exp.timestamp}")


def main():
    while True:
        print("\nExpense Tracker CLI")
        print("1. Add User")
        print("2. List Users")
        print("3. Add Category")
        print("4. List Categories")
        print("5. Add Expense")
        print("6. List Expenses")
        print("7. Filter Expenses")
        print("8. Update Expense")
        print("9. Delete Expense")
        print("10. Generate Monthly Report")
        print("0. Exit")

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
            filter_expenses()
        elif choice == "8":
            update_expense()
        elif choice == "9":
            delete_expense()
        elif choice == "10":
            generate_monthly_report()
        elif choice == "0":
            print("Goodbye!....")
            break
        else:
            print("Invalid option! Please choose again.")
       
       

if __name__ == "__main__":
    main()   
