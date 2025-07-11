import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, create_engine, DateTime, func, ForeignKey
from sqlalchemy.engine import URL



class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

class User(Base):
    __tablename__ = 'user'

    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    # password: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)



class Adverts(Base):
    __tablename__ = 'adverts'

    tittle: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[User] = mapped_column(ForeignKey("user.id"))

config = {
    'drivername': 'postgresql',
    'username': 'user',
    'password': '111',
    'host': 'localhost',
    'port': 5432,
    'database': 'Adverts1',
}


dsn = URL.create(**config)

engine = create_engine(dsn, echo=True)

Base.metadata.create_all(engine)