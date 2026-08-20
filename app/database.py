import sys
from datetime import date as date_type
from pathlib import Path

from sqlalchemy import Date, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from database_config import build_database_url

DATABASE_URL = build_database_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    amount: Mapped[float | None] = mapped_column(nullable=True)
    currency: Mapped[str | None] = mapped_column(nullable=True)
    category: Mapped[str | None] = mapped_column(nullable=True)
    account: Mapped[str | None] = mapped_column(nullable=True)
    transaction_type: Mapped[str | None] = mapped_column(nullable=True)
    month: Mapped[int | None] = mapped_column(nullable=True)
    year: Mapped[int | None] = mapped_column(nullable=True)


Base.metadata.create_all(bind=engine)
