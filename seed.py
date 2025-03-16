import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from models import Base, engine, User, Category, Expense

fake = Faker()

session = Session(bind=engine)

Base.metadata.drop_all(engine)  
Base.metadata.create_all(engine)

categories = ["Food", "Transport", "Shopping", "Entertainment", "Healthcare", "Bills", "Education"]

users = []
for _ in range(5): 
    user = User(name=fake.name(), email=fake.email())
    session.add(user)
    users.append(user)

category_objs = []
for name in categories:
    category = Category(name=name)
    session.add(category)
    category_objs.append(category)

session.commit()  


for _ in range(20):  
    amount = random.randint(100, 5000)  
    user = random.choice(users)  
    category = random.choice(category_objs)  
    timestamp = datetime.utcnow() - timedelta(days=random.randint(1, 30))  # Random past date

    expense = Expense(amount=amount, user_id=user.id, category_id=category.id, timestamp=timestamp)
    session.add(expense)

session.commit()
session.close()

print("Database seeded successfully with test data!")
