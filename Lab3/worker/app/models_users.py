from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import UsersBase


class User(UsersBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_key: Mapped[str | None] = mapped_column(Text, nullable=True)


class Subscriber(UsersBase):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False)


class NotificationSent(UsersBase):
    __tablename__ = "notifications_sent"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    post_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
