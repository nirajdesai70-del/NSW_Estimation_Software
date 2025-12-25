-- Phase-4: Lookup Pipeline Integrity Verification (PLANNING)
-- Date: 2025-12-21
-- Goal: Detect broken lookup chains that would break editability after copy/reuse/edit.
-- NOTE: Table/column names may vary by implementation; adjust joins if your schema differs.

-- =====================================================================
-- A0) Setup
-- =====================================================================
-- Use correct DB (example):
-- USE nepl_quotation;

-- =====================================================================
-- A1) Active line items baseline
-- =====================================================================
SELECT COUNT(*) AS active_items
FROM quotation_sale_bom_items
WHERE Status = 0;

-- =====================================================================
-- A2) L1: Product missing (CRITICAL)
-- =====================================================================
SELECT i.QuotationSaleBomItemId, i.ProductId
FROM quotation_sale_bom_items i
LEFT JOIN products p ON p.ProductId = i.ProductId
WHERE i.Status = 0
  AND (p.ProductId IS NULL);

-- =====================================================================
-- A3) L2: Product -> Category/SubCategory/Item(Type) broken (CRITICAL)
-- =====================================================================
SELECT 
  i.QuotationSaleBomItemId,
  i.ProductId,
  p.CategoryId,
  p.SubCategoryId,
  p.ItemId,
  CASE WHEN c.CategoryId IS NULL THEN 1 ELSE 0 END AS missing_category,
  CASE WHEN sc.SubCategoryId IS NULL THEN 1 ELSE 0 END AS missing_subcategory,
  CASE WHEN it.ItemId IS NULL THEN 1 ELSE 0 END AS missing_itemtype
FROM quotation_sale_bom_items i
JOIN products p ON p.ProductId = i.ProductId
LEFT JOIN categories c ON c.CategoryId = p.CategoryId
LEFT JOIN sub_categories sc ON sc.SubCategoryId = p.SubCategoryId
LEFT JOIN items it ON it.ItemId = p.ItemId
WHERE i.Status = 0
  AND (
    c.CategoryId IS NULL
    OR sc.SubCategoryId IS NULL
    OR it.ItemId IS NULL
  );

-- =====================================================================
-- A4) L3: Make exists + MakeCategory mapping (HIGH)
-- =====================================================================
-- Adjust make_categories join if your schema differs.
SELECT 
  i.QuotationSaleBomItemId,
  i.ProductId,
  i.MakeId,
  p.CategoryId,
  CASE WHEN m.MakeId IS NULL THEN 1 ELSE 0 END AS missing_make,
  CASE WHEN (i.MakeId <> 0 AND mc.MakeId IS NULL) THEN 1 ELSE 0 END AS make_not_allowed_for_category
FROM quotation_sale_bom_items i
JOIN products p ON p.ProductId = i.ProductId
LEFT JOIN makes m ON m.MakeId = i.MakeId
LEFT JOIN make_categories mc ON mc.MakeId = i.MakeId AND mc.CategoryId = p.CategoryId
WHERE i.Status = 0
  AND i.MakeId <> 0
  AND (m.MakeId IS NULL OR mc.MakeId IS NULL);

-- =====================================================================
-- A5) L3: Series exists + SeriesMake mapping (HIGH)
-- =====================================================================
SELECT 
  i.QuotationSaleBomItemId,
  i.ProductId,
  i.MakeId,
  i.SeriesId,
  CASE WHEN s.SeriesId IS NULL THEN 1 ELSE 0 END AS missing_series,
  CASE WHEN (i.SeriesId <> 0 AND sm.SeriesId IS NULL) THEN 1 ELSE 0 END AS series_not_allowed_for_make
FROM quotation_sale_bom_items i
LEFT JOIN series s ON s.SeriesId = i.SeriesId
LEFT JOIN series_makes sm ON sm.SeriesId = i.SeriesId AND sm.MakeId = i.MakeId
WHERE i.Status = 0
  AND i.SeriesId <> 0
  AND (s.SeriesId IS NULL OR sm.SeriesId IS NULL);

-- =====================================================================
-- A6) L4: Description as ProductId integrity (MEDIUM/HIGH depending)
-- If Description stores ProductId, validate existence.
-- If your Description is text, skip this check.
-- =====================================================================
SELECT 
  i.QuotationSaleBomItemId,
  i.ProductId AS GenericOrBaseProductId,
  i.Description AS DescriptionProductId
FROM quotation_sale_bom_items i
LEFT JOIN products pd ON pd.ProductId = i.Description
WHERE i.Status = 0
  AND i.Description IS NOT NULL
  AND i.Description <> ''
  AND i.Description REGEXP '^[0-9]+$'
  AND pd.ProductId IS NULL;

-- =====================================================================
-- A7) Summary counts (quick dashboard)
-- =====================================================================
SELECT 'L1_missing_product' AS check_name, COUNT(*) AS cnt FROM (
  SELECT i.QuotationSaleBomItemId
  FROM quotation_sale_bom_items i
  LEFT JOIN products p ON p.ProductId = i.ProductId
  WHERE i.Status = 0 AND p.ProductId IS NULL
) x
UNION ALL
SELECT 'L2_broken_category_subcat_item' AS check_name, COUNT(*) AS cnt FROM (
  SELECT i.QuotationSaleBomItemId
  FROM quotation_sale_bom_items i
  JOIN products p ON p.ProductId = i.ProductId
  LEFT JOIN categories c ON c.CategoryId = p.CategoryId
  LEFT JOIN sub_categories sc ON sc.SubCategoryId = p.SubCategoryId
  LEFT JOIN items it ON it.ItemId = p.ItemId
  WHERE i.Status = 0 AND (c.CategoryId IS NULL OR sc.SubCategoryId IS NULL OR it.ItemId IS NULL)
) y
UNION ALL
SELECT 'L3_make_invalid' AS check_name, COUNT(*) AS cnt FROM (
  SELECT i.QuotationSaleBomItemId
  FROM quotation_sale_bom_items i
  JOIN products p ON p.ProductId = i.ProductId
  LEFT JOIN makes m ON m.MakeId = i.MakeId
  LEFT JOIN make_categories mc ON mc.MakeId = i.MakeId AND mc.CategoryId = p.CategoryId
  WHERE i.Status = 0 AND i.MakeId <> 0 AND (m.MakeId IS NULL OR mc.MakeId IS NULL)
) z
UNION ALL
SELECT 'L3_series_invalid' AS check_name, COUNT(*) AS cnt FROM (
  SELECT i.QuotationSaleBomItemId
  FROM quotation_sale_bom_items i
  LEFT JOIN series s ON s.SeriesId = i.SeriesId
  LEFT JOIN series_makes sm ON sm.SeriesId = i.SeriesId AND sm.MakeId = i.MakeId
  WHERE i.Status = 0 AND i.SeriesId <> 0 AND (s.SeriesId IS NULL OR sm.SeriesId IS NULL)
) w;

-- END
