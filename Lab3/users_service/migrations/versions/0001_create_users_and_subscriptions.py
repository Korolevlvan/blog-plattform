"""create users subscriptions and notifications

Revision ID: 0001
Revises:
Create Date: 2026-03-30 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("username", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("subscription_key", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "subscribers",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("subscriber_id", sa.BigInteger(), nullable=False),
        sa.Column("author_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_unique_constraint("ux_subscribers_pair", "subscribers", ["subscriber_id", "author_id"])
    op.create_index("ix_subscribers_author_id", "subscribers", ["author_id"])

    op.create_table(
        "notifications_sent",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("subscriber_id", sa.BigInteger(), nullable=False),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("task_id", sa.String(length=255), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_unique_constraint("ux_notifications_subscriber_post", "notifications_sent", ["subscriber_id", "post_id"])


def downgrade() -> None:
    op.drop_constraint("ux_notifications_subscriber_post", "notifications_sent", type_="unique")
    op.drop_table("notifications_sent")
    op.drop_index("ix_subscribers_author_id", table_name="subscribers")
    op.drop_constraint("ux_subscribers_pair", "subscribers", type_="unique")
    op.drop_table("subscribers")
    op.drop_table("users")
