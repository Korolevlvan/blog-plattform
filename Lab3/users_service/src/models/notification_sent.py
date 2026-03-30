from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class NotificationSent(Base):
    __tablename__ = "notifications_sent"
    __table_args__ = (UniqueConstraint("subscriber_id", "post_id", name="ux_notifications_subscriber_post"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    task_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
