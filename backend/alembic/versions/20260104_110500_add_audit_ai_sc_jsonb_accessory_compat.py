"""add audit ai modules sc jsonb and accessory compatibility

Revision ID: 20260104_110500
Revises: 20260104_110400
Create Date: 2026-01-04 11:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260104_110500'
down_revision = '20260104_110400'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # AUDIT Module: audit_logs
    op.create_table('audit_logs',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.Column('resource_id', sa.BigInteger(), nullable=False),
        sa.Column('old_values', postgresql.JSONB(), nullable=True),
        sa.Column('new_values', postgresql.JSONB(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_logs_tenant_id', 'audit_logs', ['tenant_id'], unique=False)
    op.create_index('idx_audit_logs_user_id', 'audit_logs', ['user_id'], unique=False)
    op.create_index('idx_audit_logs_resource', 'audit_logs', ['resource_type', 'resource_id'], unique=False)
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'], unique=False)
    op.create_index('idx_audit_logs_created_at', 'audit_logs', ['created_at'], unique=False)

    # AUDIT Module: bom_change_logs
    op.create_table('bom_change_logs',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('bom_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('field_name', sa.String(length=100), nullable=True),
        sa.Column('before_value', sa.Text(), nullable=True),
        sa.Column('after_value', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("action IN ('CREATED', 'MODIFIED', 'ITEM_ADDED', 'ITEM_UPDATED', 'ITEM_DELETED')", name='chk_bom_change_logs_action'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['bom_id'], ['quote_boms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_bom_change_logs_tenant_id', 'bom_change_logs', ['tenant_id'], unique=False)
    op.create_index('idx_bom_change_logs_bom_id', 'bom_change_logs', ['bom_id'], unique=False)
    op.create_index('idx_bom_change_logs_user_id', 'bom_change_logs', ['user_id'], unique=False)
    op.create_index('idx_bom_change_logs_created_at', 'bom_change_logs', ['created_at'], unique=False)
    op.create_index('idx_bom_change_logs_action', 'bom_change_logs', ['action'], unique=False)

    # AI Module: ai_call_logs (Schema Reservation - Post-Phase 5 Implementation)
    op.create_table('ai_call_logs',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('quotation_id', sa.BigInteger(), nullable=True),
        sa.Column('panel_id', sa.BigInteger(), nullable=True),
        sa.Column('feeder_id', sa.BigInteger(), nullable=True),
        sa.Column('bom_item_id', sa.BigInteger(), nullable=True),
        sa.Column('endpoint', sa.String(length=100), nullable=False),
        sa.Column('request_json', postgresql.JSONB(), nullable=False),
        sa.Column('response_json', postgresql.JSONB(), nullable=False),
        sa.Column('final_action', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='OK'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("final_action IN ('ACCEPTED', 'REJECTED', 'MODIFIED')", name='chk_ai_call_logs_final_action'),
        sa.CheckConstraint("status IN ('OK', 'WARNING', 'ERROR')", name='chk_ai_call_logs_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['quotation_id'], ['quotations.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['panel_id'], ['quote_panels.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['feeder_id'], ['quote_boms.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['bom_item_id'], ['quote_bom_items.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_call_logs_tenant_id', 'ai_call_logs', ['tenant_id'], unique=False)
    op.create_index('idx_ai_call_logs_user_id', 'ai_call_logs', ['user_id'], unique=False)
    op.create_index('idx_ai_call_logs_quotation_id', 'ai_call_logs', ['quotation_id'], unique=False)
    op.create_index('idx_ai_call_logs_endpoint', 'ai_call_logs', ['endpoint'], unique=False)
    op.create_index('idx_ai_call_logs_created_at', 'ai_call_logs', ['created_at'], unique=False)

    # Decision D-SCL-01: Add sc_struct_jsonb to catalog_skus
    op.add_column('catalog_skus', sa.Column('sc_struct_jsonb', postgresql.JSONB(), nullable=False, server_default='{}'))
    op.create_index('idx_catalog_skus_sc_struct', 'catalog_skus', ['sc_struct_jsonb'], unique=False, postgresql_using='gin')

    # Decision D-ACC-01: Create accessory_compatibility table
    op.create_table('accessory_compatibility',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('parent_make', sa.String(length=100), nullable=False),
        sa.Column('parent_series_code', sa.String(length=100), nullable=False),
        sa.Column('parent_sku_code', sa.String(length=255), nullable=True),
        sa.Column('accessory_sku_code', sa.String(length=255), nullable=False),
        sa.Column('applies_to_range', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('source_page', sa.String(length=255), nullable=True),
        sa.Column('source_ref', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_accessory_compatibility_tenant_id', 'accessory_compatibility', ['tenant_id'], unique=False)
    op.create_index('idx_accessory_compatibility_parent', 'accessory_compatibility', ['parent_make', 'parent_series_code'], unique=False)
    op.create_index('idx_accessory_compatibility_parent_sku', 'accessory_compatibility', ['parent_sku_code'], unique=False)
    op.create_index('idx_accessory_compatibility_accessory', 'accessory_compatibility', ['accessory_sku_code'], unique=False)


def downgrade() -> None:
    # Drop in reverse order
    op.drop_index('idx_accessory_compatibility_accessory', table_name='accessory_compatibility')
    op.drop_index('idx_accessory_compatibility_parent_sku', table_name='accessory_compatibility')
    op.drop_index('idx_accessory_compatibility_parent', table_name='accessory_compatibility')
    op.drop_index('idx_accessory_compatibility_tenant_id', table_name='accessory_compatibility')
    op.drop_table('accessory_compatibility')
    
    op.drop_index('idx_catalog_skus_sc_struct', table_name='catalog_skus')
    op.drop_column('catalog_skus', 'sc_struct_jsonb')
    
    op.drop_index('idx_ai_call_logs_created_at', table_name='ai_call_logs')
    op.drop_index('idx_ai_call_logs_endpoint', table_name='ai_call_logs')
    op.drop_index('idx_ai_call_logs_quotation_id', table_name='ai_call_logs')
    op.drop_index('idx_ai_call_logs_user_id', table_name='ai_call_logs')
    op.drop_index('idx_ai_call_logs_tenant_id', table_name='ai_call_logs')
    op.drop_table('ai_call_logs')
    
    op.drop_index('idx_bom_change_logs_action', table_name='bom_change_logs')
    op.drop_index('idx_bom_change_logs_created_at', table_name='bom_change_logs')
    op.drop_index('idx_bom_change_logs_user_id', table_name='bom_change_logs')
    op.drop_index('idx_bom_change_logs_bom_id', table_name='bom_change_logs')
    op.drop_index('idx_bom_change_logs_tenant_id', table_name='bom_change_logs')
    op.drop_table('bom_change_logs')
    
    op.drop_index('idx_audit_logs_created_at', table_name='audit_logs')
    op.drop_index('idx_audit_logs_action', table_name='audit_logs')
    op.drop_index('idx_audit_logs_resource', table_name='audit_logs')
    op.drop_index('idx_audit_logs_user_id', table_name='audit_logs')
    op.drop_index('idx_audit_logs_tenant_id', table_name='audit_logs')
    op.drop_table('audit_logs')

