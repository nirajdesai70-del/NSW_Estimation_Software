"""create schema canon v1.0 l1/l2, quo, pricing, and other modules

Revision ID: 20260104_110400
Revises: 20260104_110309
Create Date: 2026-01-04 11:04:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260104_110400'
down_revision = '20260104_110309'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SHARED Module: cost_heads
    op.create_table('cost_heads',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("category IN ('MATERIAL', 'LABOUR', 'OTHER')", name='chk_cost_heads_category'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'code')
    )
    op.create_index('idx_cost_heads_tenant_id', 'cost_heads', ['tenant_id'], unique=False)
    op.create_index('idx_cost_heads_code', 'cost_heads', ['code'], unique=False)
    op.create_index('idx_cost_heads_category', 'cost_heads', ['category'], unique=False)
    op.create_index('idx_cost_heads_is_active', 'cost_heads', ['is_active'], unique=False)

    # CIM Module: products
    op.create_table('products',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('subcategory_id', sa.BigInteger(), nullable=True),
        sa.Column('product_type_id', sa.BigInteger(), nullable=True),
        sa.Column('generic_product_id', sa.BigInteger(), nullable=True),
        sa.Column('make_id', sa.BigInteger(), nullable=True),
        sa.Column('series_id', sa.BigInteger(), nullable=True),
        sa.Column('sku', sa.String(length=100), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cost_head_id', sa.BigInteger(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['product_type_id'], ['product_types.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['generic_product_id'], ['products.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['make_id'], ['makes.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['cost_head_id'], ['cost_heads.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_products_tenant_id', 'products', ['tenant_id'], unique=False)
    op.create_index('idx_products_category_id', 'products', ['category_id'], unique=False)
    op.create_index('idx_products_subcategory_id', 'products', ['subcategory_id'], unique=False)
    op.create_index('idx_products_product_type_id', 'products', ['product_type_id'], unique=False)
    op.create_index('idx_products_generic_product_id', 'products', ['generic_product_id'], unique=False)
    op.create_index('idx_products_make_id', 'products', ['make_id'], unique=False)
    op.create_index('idx_products_series_id', 'products', ['series_id'], unique=False)
    op.create_index('idx_products_sku', 'products', ['sku'], unique=False)
    op.create_index('idx_products_cost_head_id', 'products', ['cost_head_id'], unique=False)
    op.create_index('idx_products_is_active', 'products', ['is_active'], unique=False)
    # Partial unique index for tenant + sku
    op.execute("""
        CREATE UNIQUE INDEX idx_products_tenant_sku 
        ON products(tenant_id, sku) 
        WHERE sku IS NOT NULL
    """)

    # CIM Module: product_attributes
    op.create_table('product_attributes',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('product_id', sa.BigInteger(), nullable=False),
        sa.Column('attribute_id', sa.BigInteger(), nullable=False),
        sa.Column('value_text', sa.Text(), nullable=True),
        sa.Column('value_number', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('value_boolean', sa.Boolean(), nullable=True),
        sa.Column('value_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['attribute_id'], ['attributes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'attribute_id')
    )
    op.create_index('idx_product_attributes_tenant_id', 'product_attributes', ['tenant_id'], unique=False)
    op.create_index('idx_product_attributes_product_id', 'product_attributes', ['product_id'], unique=False)
    op.create_index('idx_product_attributes_attribute_id', 'product_attributes', ['attribute_id'], unique=False)

    # L1/L2 Module: l1_line_groups
    op.create_table('l1_line_groups',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('group_name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'group_name')
    )
    op.create_index('idx_l1_line_groups_tenant_id', 'l1_line_groups', ['tenant_id'], unique=False)
    op.create_index('idx_l1_line_groups_group_name', 'l1_line_groups', ['group_name'], unique=False)

    # L1/L2 Module: l1_intent_lines
    op.create_table('l1_intent_lines',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('subcategory_id', sa.BigInteger(), nullable=True),
        sa.Column('product_type_id', sa.BigInteger(), nullable=False),
        sa.Column('make_id', sa.BigInteger(), nullable=True),
        sa.Column('series_id', sa.BigInteger(), nullable=True),
        sa.Column('series_bucket', sa.String(length=100), nullable=True),
        sa.Column('line_type', sa.String(length=50), nullable=False),
        sa.Column('line_group_id', sa.BigInteger(), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("line_type IN ('BASE', 'FEATURE')", name='chk_l1_intent_lines_line_type'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['product_type_id'], ['product_types.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['make_id'], ['makes.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['line_group_id'], ['l1_line_groups.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_l1_intent_lines_tenant_id', 'l1_intent_lines', ['tenant_id'], unique=False)
    op.create_index('idx_l1_intent_lines_category_id', 'l1_intent_lines', ['category_id'], unique=False)
    op.create_index('idx_l1_intent_lines_product_type_id', 'l1_intent_lines', ['product_type_id'], unique=False)
    op.create_index('idx_l1_intent_lines_series_bucket', 'l1_intent_lines', ['series_bucket'], unique=False)
    op.create_index('idx_l1_intent_lines_line_type', 'l1_intent_lines', ['line_type'], unique=False)
    op.create_index('idx_l1_intent_lines_line_group_id', 'l1_intent_lines', ['line_group_id'], unique=False)
    op.create_index('idx_l1_intent_lines_is_active', 'l1_intent_lines', ['is_active'], unique=False)

    # L1/L2 Module: l1_attributes
    op.create_table('l1_attributes',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('l1_intent_line_id', sa.BigInteger(), nullable=False),
        sa.Column('attribute_code', sa.String(length=100), nullable=False),
        sa.Column('value_text', sa.Text(), nullable=True),
        sa.Column('value_number', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('value_unit', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['l1_intent_line_id'], ['l1_intent_lines.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('l1_intent_line_id', 'attribute_code')
    )
    op.create_index('idx_l1_attributes_tenant_id', 'l1_attributes', ['tenant_id'], unique=False)
    op.create_index('idx_l1_attributes_l1_intent_line_id', 'l1_attributes', ['l1_intent_line_id'], unique=False)
    op.create_index('idx_l1_attributes_attribute_code', 'l1_attributes', ['attribute_code'], unique=False)

    # Update catalog_skus to match Schema Canon (drop old columns, add new ones)
    # First, check if catalog_skus exists and has old structure
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'catalog_skus' in inspector.get_table_names():
        # Drop old columns if they exist
        columns = [col['name'] for col in inspector.get_columns('catalog_skus')]
        if 'catalog_item_id' in columns:
            op.drop_constraint('catalog_skus_catalog_item_id_fkey', 'catalog_skus', type_='foreignkey')
            op.drop_column('catalog_skus', 'catalog_item_id')
        if 'sku_type' in columns:
            op.drop_column('catalog_skus', 'sku_type')
        if 'name' in columns:
            op.drop_column('catalog_skus', 'name')
        if 'description' in columns:
            op.drop_column('catalog_skus', 'description')
        if 'series' in columns:
            op.drop_column('catalog_skus', 'series')
        if 'current_price' in columns:
            op.drop_column('catalog_skus', 'current_price')
        if 'current_currency' in columns:
            op.drop_column('catalog_skus', 'current_currency')
        if 'current_price_updated_at' in columns:
            op.drop_column('catalog_skus', 'current_price_updated_at')
        
        # Add Schema Canon columns
        if 'tenant_id' not in columns:
            op.add_column('catalog_skus', sa.Column('tenant_id', sa.BigInteger(), nullable=True))
            # Set default tenant_id (will need to be updated in data migration)
            op.execute("UPDATE catalog_skus SET tenant_id = 1 WHERE tenant_id IS NULL")
            op.alter_column('catalog_skus', 'tenant_id', nullable=False)
            op.create_foreign_key('catalog_skus_tenant_id_fkey', 'catalog_skus', 'tenants', ['tenant_id'], ['id'], ondelete='CASCADE')
        if 'oem_catalog_no' not in columns:
            op.add_column('catalog_skus', sa.Column('oem_catalog_no', sa.String(length=255), nullable=True))
            op.execute("UPDATE catalog_skus SET oem_catalog_no = sku_code WHERE oem_catalog_no IS NULL")
            op.alter_column('catalog_skus', 'oem_catalog_no', nullable=False)
        if 'oem_series_range' not in columns:
            op.add_column('catalog_skus', sa.Column('oem_series_range', sa.String(length=255), nullable=True))
        if 'series_bucket' not in columns:
            op.add_column('catalog_skus', sa.Column('series_bucket', sa.String(length=100), nullable=True))
        if 'item_producttype' not in columns:
            op.add_column('catalog_skus', sa.Column('item_producttype', sa.String(length=255), nullable=True))
        if 'business_subcategory' not in columns:
            op.add_column('catalog_skus', sa.Column('business_subcategory', sa.String(length=255), nullable=True))
        if 'source_file' not in columns:
            op.add_column('catalog_skus', sa.Column('source_file', sa.String(length=255), nullable=True))
        if 'source_page_or_table_id' not in columns:
            op.add_column('catalog_skus', sa.Column('source_page_or_table_id', sa.String(length=255), nullable=True))
        if 'source_row' not in columns:
            op.add_column('catalog_skus', sa.Column('source_row', sa.Integer(), nullable=True))
        if 'notes' not in columns:
            op.add_column('catalog_skus', sa.Column('notes', sa.Text(), nullable=True))
        
        # Update unique constraint
        op.drop_constraint('uq_catalog_sku_make_code', 'catalog_skus', type_='unique')
        op.create_unique_constraint('uq_catalog_skus_tenant_make_catalog_no', 'catalog_skus', ['tenant_id', 'make', 'oem_catalog_no'])
        
        # Update indexes
        op.drop_index('idx_catalog_sku_make_code', table_name='catalog_skus')
        op.create_index('idx_catalog_skus_tenant_id', 'catalog_skus', ['tenant_id'], unique=False)
        op.create_index('idx_catalog_skus_make', 'catalog_skus', ['make'], unique=False)
        op.create_index('idx_catalog_skus_oem_catalog_no', 'catalog_skus', ['oem_catalog_no'], unique=False)
        op.create_index('idx_catalog_skus_series_bucket', 'catalog_skus', ['series_bucket'], unique=False)
        op.create_index('idx_catalog_skus_is_active', 'catalog_skus', ['is_active'], unique=False)

    # L1/L2 Module: l1_l2_mappings
    op.create_table('l1_l2_mappings',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('l1_intent_line_id', sa.BigInteger(), nullable=False),
        sa.Column('catalog_sku_id', sa.BigInteger(), nullable=False),
        sa.Column('mapping_type', sa.String(length=50), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("mapping_type IN ('BASE', 'FEATURE_ADDON', 'FEATURE_INCLUDED', 'FEATURE_BUNDLED')", name='chk_l1_l2_mappings_mapping_type'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['l1_intent_line_id'], ['l1_intent_lines.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['catalog_sku_id'], ['catalog_skus.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_l1_l2_mappings_tenant_id', 'l1_l2_mappings', ['tenant_id'], unique=False)
    op.create_index('idx_l1_l2_mappings_l1_intent_line_id', 'l1_l2_mappings', ['l1_intent_line_id'], unique=False)
    op.create_index('idx_l1_l2_mappings_catalog_sku_id', 'l1_l2_mappings', ['catalog_sku_id'], unique=False)
    op.create_index('idx_l1_l2_mappings_mapping_type', 'l1_l2_mappings', ['mapping_type'], unique=False)

    # CUSTOMER Module: customers
    op.create_table('customers',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('ACTIVE', 'INACTIVE')", name='chk_customers_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'code')
    )
    op.create_index('idx_customers_tenant_id', 'customers', ['tenant_id'], unique=False)
    op.create_index('idx_customers_code', 'customers', ['code'], unique=False)
    op.create_index('idx_customers_status', 'customers', ['status'], unique=False)

    # MBOM Module: master_boms
    op.create_table('master_boms',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('unique_no', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('template_type', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("template_type IN ('FEEDER', 'PANEL', 'GENERIC')", name='chk_master_boms_template_type'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_master_boms_tenant_id', 'master_boms', ['tenant_id'], unique=False)
    op.create_index('idx_master_boms_unique_no', 'master_boms', ['unique_no'], unique=False)
    op.create_index('idx_master_boms_template_type', 'master_boms', ['template_type'], unique=False)
    op.create_index('idx_master_boms_is_active', 'master_boms', ['is_active'], unique=False)

    # MBOM Module: master_bom_items
    op.create_table('master_bom_items',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('master_bom_id', sa.BigInteger(), nullable=False),
        sa.Column('resolution_status', sa.String(length=10), nullable=False),
        sa.Column('generic_descriptor', sa.String(length=500), nullable=True),
        sa.Column('defined_spec_json', postgresql.JSONB(), nullable=True),
        sa.Column('product_id', sa.BigInteger(), nullable=True),
        sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=False, server_default='1.0'),
        sa.Column('uom', sa.String(length=50), nullable=True),
        sa.Column('sequence_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("resolution_status IN ('L0', 'L1')", name='chk_master_bom_items_resolution_status'),
        sa.CheckConstraint("quantity > 0", name='chk_master_bom_items_quantity'),
        sa.CheckConstraint("product_id IS NULL", name='chk_master_bom_items_no_product_id'),
        sa.CheckConstraint(
            "(resolution_status = 'L0' AND generic_descriptor IS NOT NULL AND defined_spec_json IS NULL) OR "
            "(resolution_status = 'L1' AND defined_spec_json IS NOT NULL AND generic_descriptor IS NULL)",
            name='chk_master_bom_item_l0_l1'
        ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['master_bom_id'], ['master_boms.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_master_bom_items_tenant_id', 'master_bom_items', ['tenant_id'], unique=False)
    op.create_index('idx_master_bom_items_master_bom_id', 'master_bom_items', ['master_bom_id'], unique=False)
    op.create_index('idx_master_bom_items_resolution_status', 'master_bom_items', ['resolution_status'], unique=False)

    # QUO Module: quotations
    op.create_table('quotations',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('quote_no', sa.String(length=100), nullable=False),
        sa.Column('customer_id', sa.BigInteger(), nullable=True),
        sa.Column('customer_name_snapshot', sa.String(length=255), nullable=True),
        sa.Column('project_id', sa.BigInteger(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('created_by', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('DRAFT', 'APPROVED', 'FINALIZED', 'CANCELLED')", name='chk_quotations_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'quote_no')
    )
    op.create_index('idx_quotations_tenant_id', 'quotations', ['tenant_id'], unique=False)
    op.create_index('idx_quotations_quote_no', 'quotations', ['quote_no'], unique=False)
    op.create_index('idx_quotations_customer_id', 'quotations', ['customer_id'], unique=False)
    op.create_index('idx_quotations_status', 'quotations', ['status'], unique=False)
    op.create_index('idx_quotations_created_by', 'quotations', ['created_by'], unique=False)

    # QUO Module: quote_panels
    op.create_table('quote_panels',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('quotation_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=False, server_default='1.0'),
        sa.Column('rate', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('sequence_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("quantity > 0", name='chk_quote_panels_quantity'),
        sa.CheckConstraint("rate >= 0", name='chk_quote_panels_rate'),
        sa.CheckConstraint("amount >= 0", name='chk_quote_panels_amount'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quote_panels_tenant_id', 'quote_panels', ['tenant_id'], unique=False)
    op.create_index('idx_quote_panels_quotation_id', 'quote_panels', ['quotation_id'], unique=False)
    op.create_index('idx_quote_panels_sequence_order', 'quote_panels', ['quotation_id', 'sequence_order'], unique=False)

    # QUO Module: quote_boms
    op.create_table('quote_boms',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('quotation_id', sa.BigInteger(), nullable=False),
        sa.Column('panel_id', sa.BigInteger(), nullable=False),
        sa.Column('parent_bom_id', sa.BigInteger(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=False, server_default='1.0'),
        sa.Column('rate', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('origin_master_bom_id', sa.BigInteger(), nullable=True),
        sa.Column('origin_master_bom_version', sa.String(length=50), nullable=True),
        sa.Column('instance_sequence_no', sa.Integer(), nullable=True),
        sa.Column('is_modified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('modified_by', sa.BigInteger(), nullable=True),
        sa.Column('modified_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('sequence_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("level >= 0 AND level <= 2", name='chk_quote_boms_level'),
        sa.CheckConstraint("quantity > 0", name='chk_quote_boms_quantity'),
        sa.CheckConstraint("rate >= 0", name='chk_quote_boms_rate'),
        sa.CheckConstraint("amount >= 0", name='chk_quote_boms_amount'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['panel_id'], ['quote_panels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_bom_id'], ['quote_boms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['origin_master_bom_id'], ['master_boms.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['modified_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quote_boms_tenant_id', 'quote_boms', ['tenant_id'], unique=False)
    op.create_index('idx_quote_boms_quotation_id', 'quote_boms', ['quotation_id'], unique=False)
    op.create_index('idx_quote_boms_panel_id', 'quote_boms', ['panel_id'], unique=False)
    op.create_index('idx_quote_boms_parent_bom_id', 'quote_boms', ['parent_bom_id'], unique=False)
    op.create_index('idx_quote_boms_origin_master_bom_id', 'quote_boms', ['origin_master_bom_id'], unique=False)
    op.create_index('idx_quote_boms_level', 'quote_boms', ['level'], unique=False)
    op.create_index('idx_quote_boms_is_modified', 'quote_boms', ['is_modified'], unique=False)

    # QUO Module: quote_bom_items
    op.create_table('quote_bom_items',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('quotation_id', sa.BigInteger(), nullable=False),
        sa.Column('panel_id', sa.BigInteger(), nullable=False),
        sa.Column('bom_id', sa.BigInteger(), nullable=False),
        sa.Column('parent_line_id', sa.BigInteger(), nullable=True),
        sa.Column('product_id', sa.BigInteger(), nullable=True),
        sa.Column('make_id', sa.BigInteger(), nullable=True),
        sa.Column('series_id', sa.BigInteger(), nullable=True),
        sa.Column('quantity', sa.Numeric(precision=10, scale=3), nullable=False, server_default='1.0'),
        sa.Column('rate', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('discount_pct', sa.Numeric(precision=5, scale=2), nullable=True, server_default='0'),
        sa.Column('net_rate', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('rate_source', sa.String(length=50), nullable=False, server_default='UNRESOLVED'),
        sa.Column('is_price_missing', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_client_supplied', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_locked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('cost_head_id', sa.BigInteger(), nullable=True),
        sa.Column('resolution_status', sa.String(length=10), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('metadata_json', postgresql.JSONB(), nullable=True),
        sa.Column('sequence_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("resolution_status IN ('L0', 'L1', 'L2')", name='chk_quote_bom_items_resolution_status'),
        sa.CheckConstraint("rate_source IN ('PRICELIST', 'MANUAL_WITH_DISCOUNT', 'FIXED_NO_DISCOUNT', 'UNRESOLVED')", name='chk_quote_bom_items_rate_source'),
        sa.CheckConstraint("quantity > 0", name='chk_quote_bom_items_quantity'),
        sa.CheckConstraint("rate >= 0", name='chk_quote_bom_items_rate'),
        sa.CheckConstraint("discount_pct >= 0 AND discount_pct <= 100", name='chk_quote_bom_items_discount_pct'),
        sa.CheckConstraint("net_rate >= 0", name='chk_quote_bom_items_net_rate'),
        sa.CheckConstraint("amount >= 0", name='chk_quote_bom_items_amount'),
        sa.CheckConstraint(
            "(resolution_status = 'L2' AND product_id IS NOT NULL) OR "
            "(resolution_status IN ('L0', 'L1') AND product_id IS NULL)",
            name='chk_quote_bom_item_resolution'
        ),
        sa.CheckConstraint(
            "(rate_source = 'FIXED_NO_DISCOUNT' AND discount_pct = 0) OR "
            "(rate_source != 'FIXED_NO_DISCOUNT')",
            name='chk_quote_bom_item_rate_source'
        ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['panel_id'], ['quote_panels.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['bom_id'], ['quote_boms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_line_id'], ['quote_bom_items.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['make_id'], ['makes.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['series_id'], ['series.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['cost_head_id'], ['cost_heads.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quote_bom_items_tenant_id', 'quote_bom_items', ['tenant_id'], unique=False)
    op.create_index('idx_quote_bom_items_quotation_id', 'quote_bom_items', ['quotation_id'], unique=False)
    op.create_index('idx_quote_bom_items_panel_id', 'quote_bom_items', ['panel_id'], unique=False)
    op.create_index('idx_quote_bom_items_bom_id', 'quote_bom_items', ['bom_id'], unique=False)
    op.create_index('idx_quote_bom_items_parent_line_id', 'quote_bom_items', ['parent_line_id'], unique=False)
    op.create_index('idx_quote_bom_items_product_id', 'quote_bom_items', ['product_id'], unique=False)
    op.create_index('idx_quote_bom_items_cost_head_id', 'quote_bom_items', ['cost_head_id'], unique=False)
    op.create_index('idx_quote_bom_items_resolution_status', 'quote_bom_items', ['resolution_status'], unique=False)
    op.create_index('idx_quote_bom_items_rate_source', 'quote_bom_items', ['rate_source'], unique=False)
    op.create_index('idx_quote_bom_items_is_locked', 'quote_bom_items', ['is_locked'], unique=False)
    op.create_index('idx_quote_bom_items_is_price_missing', 'quote_bom_items', ['is_price_missing'], unique=False)

    # QUO Module: quote_bom_item_history
    op.create_table('quote_bom_item_history',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('quote_bom_item_id', sa.BigInteger(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('changed_by', sa.BigInteger(), nullable=True),
        sa.Column('old_values', postgresql.JSONB(), nullable=True),
        sa.Column('new_values', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("action IN ('CREATED', 'UPDATED', 'DELETED', 'RESOLVED', 'PRICE_CHANGED')", name='chk_quote_bom_item_history_action'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['quote_bom_item_id'], ['quote_bom_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_quote_bom_item_history_tenant_id', 'quote_bom_item_history', ['tenant_id'], unique=False)
    op.create_index('idx_quote_bom_item_history_item_id', 'quote_bom_item_history', ['quote_bom_item_id'], unique=False)
    op.create_index('idx_quote_bom_item_history_created_at', 'quote_bom_item_history', ['created_at'], unique=False)
    op.create_index('idx_quote_bom_item_history_action', 'quote_bom_item_history', ['action'], unique=False)

    # PRICING Module: Update price_lists to match Schema Canon
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'price_lists' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('price_lists')]
        if 'tenant_id' not in columns:
            op.add_column('price_lists', sa.Column('tenant_id', sa.BigInteger(), nullable=True))
            op.execute("UPDATE price_lists SET tenant_id = 1 WHERE tenant_id IS NULL")
            op.alter_column('price_lists', 'tenant_id', nullable=False)
            op.create_foreign_key('price_lists_tenant_id_fkey', 'price_lists', 'tenants', ['tenant_id'], ['id'], ondelete='CASCADE')
        if 'code' not in columns:
            op.add_column('price_lists', sa.Column('code', sa.String(length=100), nullable=True))
            op.execute("UPDATE price_lists SET code = name WHERE code IS NULL")
            op.alter_column('price_lists', 'code', nullable=False)
        if 'effective_date' not in columns and 'effective_from' in columns:
            op.alter_column('price_lists', 'effective_from', new_column_name='effective_date')
        elif 'effective_date' not in columns:
            op.add_column('price_lists', sa.Column('effective_date', sa.Date(), nullable=True))
            op.execute("UPDATE price_lists SET effective_date = CURRENT_DATE WHERE effective_date IS NULL")
            op.alter_column('price_lists', 'effective_date', nullable=False)
        if 'effective_to' in columns:
            op.drop_column('price_lists', 'effective_to')
        
        op.create_index('idx_price_lists_tenant_id', 'price_lists', ['tenant_id'], unique=False)
        op.create_index('idx_price_lists_code', 'price_lists', ['code'], unique=False)
        op.create_index('idx_price_lists_effective_date', 'price_lists', ['effective_date'], unique=False)
        op.create_index('idx_price_lists_is_active', 'price_lists', ['is_active'], unique=False)
        op.create_unique_constraint('uq_price_lists_tenant_code', 'price_lists', ['tenant_id', 'code'])

    # PRICING Module: prices (for products)
    op.create_table('prices',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('product_id', sa.BigInteger(), nullable=False),
        sa.Column('price_list_id', sa.BigInteger(), nullable=True),
        sa.Column('rate', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('effective_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("rate >= 0", name='chk_prices_rate'),
        sa.CheckConstraint("status IN ('ACTIVE', 'DELETED')", name='chk_prices_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['price_list_id'], ['price_lists.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_prices_tenant_id', 'prices', ['tenant_id'], unique=False)
    op.create_index('idx_prices_product_id', 'prices', ['product_id'], unique=False)
    op.create_index('idx_prices_price_list_id', 'prices', ['price_list_id'], unique=False)
    op.create_index('idx_prices_effective_date', 'prices', ['effective_date'], unique=False)
    op.create_index('idx_prices_status', 'prices', ['status'], unique=False)
    op.execute("""
        CREATE INDEX idx_prices_lookup 
        ON prices(product_id, effective_date, status) 
        WHERE status = 'ACTIVE'
    """)

    # PRICING Module: Update sku_prices to match Schema Canon
    if 'sku_prices' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('sku_prices')]
        if 'tenant_id' not in columns:
            op.add_column('sku_prices', sa.Column('tenant_id', sa.BigInteger(), nullable=True))
            op.execute("UPDATE sku_prices SET tenant_id = 1 WHERE tenant_id IS NULL")
            op.alter_column('sku_prices', 'tenant_id', nullable=False)
            op.create_foreign_key('sku_prices_tenant_id_fkey', 'sku_prices', 'tenants', ['tenant_id'], ['id'], ondelete='CASCADE')
        if 'catalog_sku_id' not in columns and 'sku_id' in columns:
            op.alter_column('sku_prices', 'sku_id', new_column_name='catalog_sku_id')
        elif 'catalog_sku_id' not in columns:
            op.add_column('sku_prices', sa.Column('catalog_sku_id', sa.BigInteger(), nullable=True))
            op.execute("UPDATE sku_prices SET catalog_sku_id = sku_id WHERE catalog_sku_id IS NULL")
            op.alter_column('sku_prices', 'catalog_sku_id', nullable=False)
            op.create_foreign_key('sku_prices_catalog_sku_id_fkey', 'sku_prices', 'catalog_skus', ['catalog_sku_id'], ['id'], ondelete='CASCADE')
        if 'pricelist_ref' not in columns:
            op.add_column('sku_prices', sa.Column('pricelist_ref', sa.String(length=255), nullable=True))
            op.execute("UPDATE sku_prices SET pricelist_ref = 'DEFAULT' WHERE pricelist_ref IS NULL")
            op.alter_column('sku_prices', 'pricelist_ref', nullable=False)
        if 'rate' not in columns and 'price' in columns:
            op.alter_column('sku_prices', 'price', new_column_name='rate')
        elif 'rate' not in columns:
            op.add_column('sku_prices', sa.Column('rate', sa.Numeric(precision=15, scale=2), nullable=True))
            op.execute("UPDATE sku_prices SET rate = price WHERE rate IS NULL")
            op.alter_column('sku_prices', 'rate', nullable=False)
        if 'currency' not in columns:
            op.add_column('sku_prices', sa.Column('currency', sa.String(length=10), nullable=True, server_default='INR'))
            op.alter_column('sku_prices', 'currency', nullable=False)
        if 'region' not in columns:
            op.add_column('sku_prices', sa.Column('region', sa.String(length=100), nullable=True, server_default='INDIA'))
            op.alter_column('sku_prices', 'region', nullable=False)
        if 'effective_from' not in columns:
            op.add_column('sku_prices', sa.Column('effective_from', sa.Date(), nullable=True))
            op.execute("UPDATE sku_prices SET effective_from = CURRENT_DATE WHERE effective_from IS NULL")
            op.alter_column('sku_prices', 'effective_from', nullable=False)
        if 'effective_to' not in columns:
            op.add_column('sku_prices', sa.Column('effective_to', sa.Date(), nullable=True))
        
        op.create_index('idx_sku_prices_tenant_id', 'sku_prices', ['tenant_id'], unique=False)
        op.create_index('idx_sku_prices_catalog_sku_id', 'sku_prices', ['catalog_sku_id'], unique=False)
        op.create_index('idx_sku_prices_price_list_id', 'sku_prices', ['price_list_id'], unique=False)
        op.create_index('idx_sku_prices_pricelist_ref', 'sku_prices', ['pricelist_ref'], unique=False)
        op.create_index('idx_sku_prices_effective_from', 'sku_prices', ['effective_from'], unique=False)
        op.create_index('idx_sku_prices_effective_to', 'sku_prices', ['effective_to'], unique=False)
        op.execute("""
            CREATE INDEX idx_sku_prices_lookup 
            ON sku_prices(catalog_sku_id, effective_from, effective_to) 
            WHERE effective_to IS NULL OR effective_to >= CURRENT_DATE
        """)

    # PRICING Module: import_batches
    op.create_table('import_batches',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('price_list_id', sa.BigInteger(), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('total_rows', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('processed_rows', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('error_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('imported_by', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')", name='chk_import_batches_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['price_list_id'], ['price_lists.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['imported_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_import_batches_tenant_id', 'import_batches', ['tenant_id'], unique=False)
    op.create_index('idx_import_batches_price_list_id', 'import_batches', ['price_list_id'], unique=False)
    op.create_index('idx_import_batches_status', 'import_batches', ['status'], unique=False)

    # PRICING Module: import_approval_queue
    op.create_table('import_approval_queue',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('import_batch_id', sa.BigInteger(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING'),
        sa.Column('requested_by', sa.BigInteger(), nullable=False),
        sa.Column('approved_by', sa.BigInteger(), nullable=True),
        sa.Column('approved_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('PENDING', 'APPROVED', 'REJECTED')", name='chk_import_approval_queue_status'),
        sa.ForeignKeyConstraint(['import_batch_id'], ['import_batches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['requested_by'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_import_approval_queue_import_batch_id', 'import_approval_queue', ['import_batch_id'], unique=False)
    op.create_index('idx_import_approval_queue_status', 'import_approval_queue', ['status'], unique=False)


def downgrade() -> None:
    # Drop in reverse order
    op.drop_index('idx_import_approval_queue_status', table_name='import_approval_queue')
    op.drop_index('idx_import_approval_queue_import_batch_id', table_name='import_approval_queue')
    op.drop_table('import_approval_queue')
    
    op.drop_index('idx_import_batches_status', table_name='import_batches')
    op.drop_index('idx_import_batches_price_list_id', table_name='import_batches')
    op.drop_index('idx_import_batches_tenant_id', table_name='import_batches')
    op.drop_table('import_batches')
    
    op.drop_index('idx_quote_bom_item_history_action', table_name='quote_bom_item_history')
    op.drop_index('idx_quote_bom_item_history_created_at', table_name='quote_bom_item_history')
    op.drop_index('idx_quote_bom_item_history_item_id', table_name='quote_bom_item_history')
    op.drop_index('idx_quote_bom_item_history_tenant_id', table_name='quote_bom_item_history')
    op.drop_table('quote_bom_item_history')
    
    op.drop_index('idx_quote_bom_items_is_price_missing', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_is_locked', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_rate_source', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_resolution_status', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_cost_head_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_product_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_parent_line_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_bom_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_panel_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_quotation_id', table_name='quote_bom_items')
    op.drop_index('idx_quote_bom_items_tenant_id', table_name='quote_bom_items')
    op.drop_table('quote_bom_items')
    
    op.drop_index('idx_quote_boms_is_modified', table_name='quote_boms')
    op.drop_index('idx_quote_boms_level', table_name='quote_boms')
    op.drop_index('idx_quote_boms_origin_master_bom_id', table_name='quote_boms')
    op.drop_index('idx_quote_boms_parent_bom_id', table_name='quote_boms')
    op.drop_index('idx_quote_boms_panel_id', table_name='quote_boms')
    op.drop_index('idx_quote_boms_quotation_id', table_name='quote_boms')
    op.drop_index('idx_quote_boms_tenant_id', table_name='quote_boms')
    op.drop_table('quote_boms')
    
    op.drop_index('idx_quote_panels_sequence_order', table_name='quote_panels')
    op.drop_index('idx_quote_panels_quotation_id', table_name='quote_panels')
    op.drop_index('idx_quote_panels_tenant_id', table_name='quote_panels')
    op.drop_table('quote_panels')
    
    op.drop_index('idx_quotations_created_by', table_name='quotations')
    op.drop_index('idx_quotations_status', table_name='quotations')
    op.drop_index('idx_quotations_customer_id', table_name='quotations')
    op.drop_index('idx_quotations_quote_no', table_name='quotations')
    op.drop_index('idx_quotations_tenant_id', table_name='quotations')
    op.drop_table('quotations')
    
    op.drop_index('idx_master_bom_items_resolution_status', table_name='master_bom_items')
    op.drop_index('idx_master_bom_items_master_bom_id', table_name='master_bom_items')
    op.drop_index('idx_master_bom_items_tenant_id', table_name='master_bom_items')
    op.drop_table('master_bom_items')
    
    op.drop_index('idx_master_boms_is_active', table_name='master_boms')
    op.drop_index('idx_master_boms_template_type', table_name='master_boms')
    op.drop_index('idx_master_boms_unique_no', table_name='master_boms')
    op.drop_index('idx_master_boms_tenant_id', table_name='master_boms')
    op.drop_table('master_boms')
    
    op.drop_index('idx_customers_status', table_name='customers')
    op.drop_index('idx_customers_code', table_name='customers')
    op.drop_index('idx_customers_tenant_id', table_name='customers')
    op.drop_table('customers')
    
    op.drop_index('idx_l1_l2_mappings_mapping_type', table_name='l1_l2_mappings')
    op.drop_index('idx_l1_l2_mappings_catalog_sku_id', table_name='l1_l2_mappings')
    op.drop_index('idx_l1_l2_mappings_l1_intent_line_id', table_name='l1_l2_mappings')
    op.drop_index('idx_l1_l2_mappings_tenant_id', table_name='l1_l2_mappings')
    op.drop_table('l1_l2_mappings')
    
    op.drop_index('idx_l1_attributes_attribute_code', table_name='l1_attributes')
    op.drop_index('idx_l1_attributes_l1_intent_line_id', table_name='l1_attributes')
    op.drop_index('idx_l1_attributes_tenant_id', table_name='l1_attributes')
    op.drop_table('l1_attributes')
    
    op.drop_index('idx_l1_intent_lines_is_active', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_line_group_id', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_line_type', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_series_bucket', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_product_type_id', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_category_id', table_name='l1_intent_lines')
    op.drop_index('idx_l1_intent_lines_tenant_id', table_name='l1_intent_lines')
    op.drop_table('l1_intent_lines')
    
    op.drop_index('idx_l1_line_groups_group_name', table_name='l1_line_groups')
    op.drop_index('idx_l1_line_groups_tenant_id', table_name='l1_line_groups')
    op.drop_table('l1_line_groups')
    
    op.drop_index('idx_product_attributes_attribute_id', table_name='product_attributes')
    op.drop_index('idx_product_attributes_product_id', table_name='product_attributes')
    op.drop_index('idx_product_attributes_tenant_id', table_name='product_attributes')
    op.drop_table('product_attributes')
    
    op.execute("DROP INDEX IF EXISTS idx_products_tenant_sku")
    op.drop_index('idx_products_is_active', table_name='products')
    op.drop_index('idx_products_cost_head_id', table_name='products')
    op.drop_index('idx_products_sku', table_name='products')
    op.drop_index('idx_products_series_id', table_name='products')
    op.drop_index('idx_products_make_id', table_name='products')
    op.drop_index('idx_products_generic_product_id', table_name='products')
    op.drop_index('idx_products_product_type_id', table_name='products')
    op.drop_index('idx_products_subcategory_id', table_name='products')
    op.drop_index('idx_products_category_id', table_name='products')
    op.drop_index('idx_products_tenant_id', table_name='products')
    op.drop_table('products')
    
    op.drop_index('idx_cost_heads_is_active', table_name='cost_heads')
    op.drop_index('idx_cost_heads_category', table_name='cost_heads')
    op.drop_index('idx_cost_heads_code', table_name='cost_heads')
    op.drop_index('idx_cost_heads_tenant_id', table_name='cost_heads')
    op.drop_table('cost_heads')

