"""catalog current price + skuprice audit + make nullable

Revision ID: 6fbca98f32b1
Revises: 
Create Date: 2025-12-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6fbca98f32b1'
down_revision = 'f43171814116'  # Depends on create_catalog_tables migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make CatalogSku.make non-nullable (required for unique constraint)
    # First, check if table exists and ensure all existing rows have a make value
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'catalog_skus' in inspector.get_table_names():
        op.execute("""
            UPDATE catalog_skus 
            SET make = 'UNKNOWN' 
            WHERE make IS NULL
        """)
        
        # Now alter the column to be non-nullable
        op.alter_column('catalog_skus', 'make',
                        existing_type=sa.String(length=100),
                        nullable=False,
                        existing_nullable=True)


def downgrade() -> None:
    # Revert make back to nullable
    op.alter_column('catalog_skus', 'make',
                    existing_type=sa.String(length=100),
                    nullable=True,
                    existing_nullable=False)

