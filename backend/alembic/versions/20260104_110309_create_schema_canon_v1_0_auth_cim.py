"""create schema canon v1.0 auth and cim modules

Revision ID: 20260104_110309
Revises: 6fbca98f32b1
Create Date: 2026-01-04 11:03:09.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260104_110309'
down_revision = '6fbca98f32b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # AUTH Module: tenants
    op.create_table('tenants',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ACTIVE'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('ACTIVE', 'INACTIVE')", name='chk_tenants_status'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('idx_tenants_code', 'tenants', ['code'], unique=False)
    op.create_index('idx_tenants_status', 'tenants', ['status'], unique=False)

    # AUTH Module: users
    op.create_table('users',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='ACTIVE'),
        sa.Column('email_verified_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("status IN ('ACTIVE', 'INACTIVE')", name='chk_users_status'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'email')
    )
    op.create_index('idx_users_tenant_id', 'users', ['tenant_id'], unique=False)
    op.create_index('idx_users_email', 'users', ['email'], unique=False)
    op.create_index('idx_users_status', 'users', ['status'], unique=False)

    # AUTH Module: roles
    op.create_table('roles',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'name')
    )
    op.create_index('idx_roles_tenant_id', 'roles', ['tenant_id'], unique=False)

    # AUTH Module: user_roles
    op.create_table('user_roles',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('role_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'role_id')
    )
    op.create_index('idx_user_roles_user_id', 'user_roles', ['user_id'], unique=False)
    op.create_index('idx_user_roles_role_id', 'user_roles', ['role_id'], unique=False)

    # AUTH Module: permissions (optional, reserved for future)
    op.create_table('permissions',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('resource', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'resource', 'action')
    )
    op.create_index('idx_permissions_tenant_id', 'permissions', ['tenant_id'], unique=False)
    op.create_index('idx_permissions_resource', 'permissions', ['resource'], unique=False)

    # AUTH Module: role_permissions (optional, reserved for future)
    op.create_table('role_permissions',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('role_id', sa.BigInteger(), nullable=False),
        sa.Column('permission_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('role_id', 'permission_id')
    )
    op.create_index('idx_role_permissions_role_id', 'role_permissions', ['role_id'], unique=False)
    op.create_index('idx_role_permissions_permission_id', 'role_permissions', ['permission_id'], unique=False)

    # CIM Module: categories
    op.create_table('categories',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'code')
    )
    op.create_index('idx_categories_tenant_id', 'categories', ['tenant_id'], unique=False)
    op.create_index('idx_categories_code', 'categories', ['code'], unique=False)
    op.create_index('idx_categories_is_active', 'categories', ['is_active'], unique=False)

    # CIM Module: subcategories
    op.create_table('subcategories',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'category_id', 'code')
    )
    op.create_index('idx_subcategories_tenant_id', 'subcategories', ['tenant_id'], unique=False)
    op.create_index('idx_subcategories_category_id', 'subcategories', ['category_id'], unique=False)
    op.create_index('idx_subcategories_is_active', 'subcategories', ['is_active'], unique=False)

    # CIM Module: product_types
    op.create_table('product_types',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'category_id', 'code')
    )
    op.create_index('idx_product_types_tenant_id', 'product_types', ['tenant_id'], unique=False)
    op.create_index('idx_product_types_category_id', 'product_types', ['category_id'], unique=False)
    op.create_index('idx_product_types_is_active', 'product_types', ['is_active'], unique=False)

    # CIM Module: attributes
    op.create_table('attributes',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('data_type', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("data_type IN ('TEXT', 'NUMBER', 'ENUM', 'BOOLEAN', 'DATE')", name='chk_attributes_data_type'),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'name')
    )
    op.create_index('idx_attributes_tenant_id', 'attributes', ['tenant_id'], unique=False)
    op.create_index('idx_attributes_is_active', 'attributes', ['is_active'], unique=False)

    # CIM Module: category_attributes
    op.create_table('category_attributes',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('attribute_id', sa.BigInteger(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['attribute_id'], ['attributes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category_id', 'attribute_id')
    )
    op.create_index('idx_category_attributes_tenant_id', 'category_attributes', ['tenant_id'], unique=False)
    op.create_index('idx_category_attributes_category_id', 'category_attributes', ['category_id'], unique=False)
    op.create_index('idx_category_attributes_attribute_id', 'category_attributes', ['attribute_id'], unique=False)

    # CIM Module: makes
    op.create_table('makes',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'name')
    )
    op.create_index('idx_makes_tenant_id', 'makes', ['tenant_id'], unique=False)
    op.create_index('idx_makes_is_active', 'makes', ['is_active'], unique=False)

    # CIM Module: series
    op.create_table('series',
        sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
        sa.Column('tenant_id', sa.BigInteger(), nullable=False),
        sa.Column('make_id', sa.BigInteger(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['make_id'], ['makes.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id', 'make_id', 'name')
    )
    op.create_index('idx_series_tenant_id', 'series', ['tenant_id'], unique=False)
    op.create_index('idx_series_make_id', 'series', ['make_id'], unique=False)
    op.create_index('idx_series_is_active', 'series', ['is_active'], unique=False)


def downgrade() -> None:
    # Drop in reverse order
    op.drop_index('idx_series_is_active', table_name='series')
    op.drop_index('idx_series_make_id', table_name='series')
    op.drop_index('idx_series_tenant_id', table_name='series')
    op.drop_table('series')
    
    op.drop_index('idx_makes_is_active', table_name='makes')
    op.drop_index('idx_makes_tenant_id', table_name='makes')
    op.drop_table('makes')
    
    op.drop_index('idx_category_attributes_attribute_id', table_name='category_attributes')
    op.drop_index('idx_category_attributes_category_id', table_name='category_attributes')
    op.drop_index('idx_category_attributes_tenant_id', table_name='category_attributes')
    op.drop_table('category_attributes')
    
    op.drop_index('idx_attributes_is_active', table_name='attributes')
    op.drop_index('idx_attributes_tenant_id', table_name='attributes')
    op.drop_table('attributes')
    
    op.drop_index('idx_product_types_is_active', table_name='product_types')
    op.drop_index('idx_product_types_category_id', table_name='product_types')
    op.drop_index('idx_product_types_tenant_id', table_name='product_types')
    op.drop_table('product_types')
    
    op.drop_index('idx_subcategories_is_active', table_name='subcategories')
    op.drop_index('idx_subcategories_category_id', table_name='subcategories')
    op.drop_index('idx_subcategories_tenant_id', table_name='subcategories')
    op.drop_table('subcategories')
    
    op.drop_index('idx_categories_is_active', table_name='categories')
    op.drop_index('idx_categories_code', table_name='categories')
    op.drop_index('idx_categories_tenant_id', table_name='categories')
    op.drop_table('categories')
    
    op.drop_index('idx_role_permissions_permission_id', table_name='role_permissions')
    op.drop_index('idx_role_permissions_role_id', table_name='role_permissions')
    op.drop_table('role_permissions')
    
    op.drop_index('idx_permissions_resource', table_name='permissions')
    op.drop_index('idx_permissions_tenant_id', table_name='permissions')
    op.drop_table('permissions')
    
    op.drop_index('idx_user_roles_role_id', table_name='user_roles')
    op.drop_index('idx_user_roles_user_id', table_name='user_roles')
    op.drop_table('user_roles')
    
    op.drop_index('idx_roles_tenant_id', table_name='roles')
    op.drop_table('roles')
    
    op.drop_index('idx_users_status', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_index('idx_users_tenant_id', table_name='users')
    op.drop_table('users')
    
    op.drop_index('idx_tenants_status', table_name='tenants')
    op.drop_index('idx_tenants_code', table_name='tenants')
    op.drop_table('tenants')

