from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    _amount = Column("amount", Integer, nullable=False)  # Private variable for validation
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Expense amount must be a positive integer.")
        self._amount = value

    def __repr__(self):
        return f"<Expense(amount={self.amount}, user_id={self.user_id}, category_id={self.category_id})>"
