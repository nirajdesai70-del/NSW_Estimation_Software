"""add category_id to quote_bom_items (Phase-5 P0-N2)

Revision ID: 20260127_093000
Revises: 20260127_090000
Create Date: 2026-01-27 09:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20260127_093000"
down_revision = "20260127_090000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "quote_bom_items",
        sa.Column("category_id", sa.BigInteger(), nullable=True),
    )

    op.create_foreign_key(
        "fk_quote_bom_items_category_id",
        "quote_bom_items",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_index(
        "idx_quote_bom_items_category_id",
        "quote_bom_items",
        ["quotation_id", "category_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_quote_bom_items_category_id", table_name="quote_bom_items")
    op.drop_constraint("fk_quote_bom_items_category_id", "quote_bom_items", type_="foreignkey")
    op.drop_column("quote_bom_items", "category_id")

