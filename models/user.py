from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One-to-Many: Expenses
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
