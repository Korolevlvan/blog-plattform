from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"
    __table_args__ = (UniqueConstraint("subscriber_id", "author_id", name="ux_subscribers_pair"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
