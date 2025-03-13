from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # One-to-Many: Expenses
    expenses = relationship("Expense", back_populates="category", cascade="all, delete")

    def __repr__(self):
        return f"<Category(name={self.name})>"
