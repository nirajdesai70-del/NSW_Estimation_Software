"""
Catalog Models
SKU-first design per ADR-0001
"""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class SKUType(PyEnum):
    """SKU type enumeration per ADR-0001"""
    PRIMARY = "PRIMARY"  # Main SKU for catalog item
    BUILT_IN = "BUILT_IN"  # Addon bundled into main SKU
    ADDON = "ADDON"  # Optional addon, separate SKU
    OPTIONAL = "OPTIONAL"  # Optional component
    MANDATORY_SPLIT = "MANDATORY_SPLIT"  # Required separate SKU


class CatalogItem(Base):
    """
    Catalog Item (L1)
    Grouping/browse entity. Pricing truth is at SKU level.
    """
    __tablename__ = "catalog_items"

    id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    make = Column(String(100), nullable=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    skus = relationship("CatalogSku", back_populates="catalog_item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CatalogItem(id={self.id}, item_code='{self.item_code}', name='{self.name}')>"


class CatalogSku(Base):
    """
    Catalog SKU
    Pricing truth. One item can have multiple SKUs.
    """
    __tablename__ = "catalog_skus"

    id = Column(Integer, primary_key=True, index=True)
    catalog_item_id = Column(Integer, ForeignKey("catalog_items.id", ondelete="CASCADE"), nullable=False, index=True)
    sku_code = Column(String(100), nullable=False, index=True)
    sku_type = Column(Enum(SKUType), nullable=False, default=SKUType.PRIMARY)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    series = Column(String(200), nullable=True, index=True)  # Product series (e.g., "Easy TeSys Power Contactors (LC1E, 3P)")
    make = Column(String(100), nullable=False, index=True)
    uom = Column(String(20), nullable=True)  # Unit of measure
    
    # Current price snapshot (fast quoting - Option-1)
    current_price = Column(Numeric(12, 2), nullable=True)
    current_currency = Column(String(3), default="INR", nullable=False)
    current_price_updated_at = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    catalog_item = relationship("CatalogItem", back_populates="skus")
    prices = relationship("SkuPrice", back_populates="sku", cascade="all, delete-orphan")

    # Unique constraint: make + sku_code must be unique
    __table_args__ = (
        UniqueConstraint("make", "sku_code", name="uq_catalog_sku_make_code"),
        Index("idx_catalog_sku_make_code", "make", "sku_code"),
    )

    def __repr__(self):
        return f"<CatalogSku(id={self.id}, sku_code='{self.sku_code}', type='{self.sku_type.value}')>"


class PriceList(Base):
    """
    Price List
    Container for SKU prices with effective dates
    """
    __tablename__ = "price_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    currency = Column(String(3), default="INR", nullable=False)
    effective_from = Column(DateTime, nullable=False, index=True)
    effective_to = Column(DateTime, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    prices = relationship("SkuPrice", back_populates="price_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PriceList(id={self.id}, name='{self.name}', currency='{self.currency}')>"


class SkuPrice(Base):
    """
    SKU Price
    SKU-level pricing (pricing truth per ADR-0001)
    """
    __tablename__ = "sku_prices"

    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(Integer, ForeignKey("catalog_skus.id", ondelete="CASCADE"), nullable=False, index=True)
    price_list_id = Column(Integer, ForeignKey("price_lists.id", ondelete="CASCADE"), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    effective_from = Column(DateTime, nullable=False, index=True)
    effective_to = Column(DateTime, nullable=True, index=True)
    
    # Audit fields for import tracking
    import_batch_id = Column(String(36), nullable=True, index=True)  # UUID string
    source_file = Column(Text, nullable=True)  # Source filename
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    sku = relationship("CatalogSku", back_populates="prices")
    price_list = relationship("PriceList", back_populates="prices")

    # Unique constraint: one price per SKU per price list
    __table_args__ = (
        UniqueConstraint("sku_id", "price_list_id", name="uq_sku_price_list"),
        Index("idx_sku_price_effective", "sku_id", "effective_from", "effective_to"),
    )

    def __repr__(self):
        return f"<SkuPrice(id={self.id}, sku_id={self.sku_id}, price={self.price})>"

