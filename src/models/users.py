from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from src.database import Base

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped [int] = mapped_column(primary_key=True)
    email: Mapped [str] = mapped_column(String(200))
    hashed_password: Mapped [str] = mapped_column(String(200))
