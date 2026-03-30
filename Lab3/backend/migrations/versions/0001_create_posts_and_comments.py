"""create posts and comments

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
        "posts",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False, unique=True),
        sa.Column("tag_list", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_posts_user_id", "posts", ["user_id"])

    op.create_table(
        "comments",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("post_id", sa.BigInteger(), sa.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_comments_post_id", "comments", ["post_id"])


def downgrade() -> None:
    op.drop_index("ix_comments_post_id", table_name="comments")
    op.drop_table("comments")
    op.drop_index("ix_posts_user_id", table_name="posts")
    op.drop_table("posts")
