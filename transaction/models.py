from sqlalchemy import String, DateTime, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database.core import Base
from transaction.schemas import Currency

from datetime import datetime


class Transactions(Base):
	__tablename__ = "transactions"

	id: Mapped[str] = mapped_column(String(6), primary_key=True)
	user_id: Mapped[str] = mapped_column(String(300), nullable=False)
	amount: Mapped[float] = mapped_column(Float, nullable=False)
	currency: Mapped[str] = mapped_column(Enum(*[e.value for e in Currency], name='currency_type'), nullable=False)
	timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

load = lambda: None