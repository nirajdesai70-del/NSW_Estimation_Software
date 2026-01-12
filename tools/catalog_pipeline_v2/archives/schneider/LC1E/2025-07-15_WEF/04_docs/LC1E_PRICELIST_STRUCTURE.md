# LC1E Pricelist Structure Analysis

## File Location
- XLSX: `input/schneider/lc1e/Switching _All_WEF 15th Jul 25.xlsx`
- Sheet: `Table 1` (single sheet, 1485+ rows)

## Structure Overview

The pricelist uses a complex format with merged cells and multiple sections. LC1E data appears in several sections:

### Section 1: LC1E 3P AC Control (Rows ~40-75)

**Header Row (Row 41-42):**
- Col15: AC-1
- Col23: AC-3
- Col32: HP
- Col41: kW
- Col50: NO (aux contacts)
- Col61: NC (aux contacts)
- Note: Coil code columns (M7, N5) appear later or in separate sections

**Data Row Pattern (Rows 42-74):**
- Col15: AC-1 current (e.g., "20 A", "25 A")
- Col23: AC-3 current (e.g., "6 A", "9 A")
- Col32: HP rating
- Col41: kW rating
- Col50: NO aux count (1 or "-")
- Col61: NC aux count (1 or "-")
- SKU appears in column (needs verification - appears as LC1E0601, LC1E0610, etc.)

### Section 2: LC1E Higher Frames 3P AC (Rows ~66-74)

**Header Row (Row 66):**
- Col15: AC-1
- Col23: AC-3
- Col32: HP
- Col37: kW
- Col43: NO
- Col50: NC
- Col61: **M7 (220V)** ← Price column
- Col70: **N5 (415)** ← Price column
- Col76: **M5 (220V)** ← Price column

**Data Rows (67-74):**
- Col0: Frame label (e.g., "FRAME-5", "FRAME-6")
- Col15: AC-1 current (e.g., "150 A")
- Col23: AC-3 current (e.g., "120 A")
- Col32: HP
- Col37: kW
- Col43: NO aux (1 or "-")
- Col50: NC aux (1 or "-")
- Col53: **Base SKU with asterisk** (e.g., "LC1E120*", "LC1E160*")
- Col61: **M7 price** (numeric or "-")
- Col70: **N5 price** (numeric or "-")
- Col76: **M5 price** (numeric or "-")

**Example Row 67:**
- Base: LC1E120*
- AC1: 150 A, AC3: 120 A
- HP: 75, kW: 55
- NO: 1, NC: 1
- M7: -, N5: 29190, M5: 29190

### Section 3: LC1E 3P DC Control (Row ~83+)

**Header Row (Row 83):**
- Col8: AC-1
- Col21: AC-3
- Col32: HP
- Col35: kW
- Col44: NO
- Col55: NC
- Note: BD coil code column needs to be located

**Data Rows (84+):**
- Similar structure to Section 1, but with BD prices
- SKUs appear as LC1E0601*, LC1E0610*, etc.

### Section 4: LC1E 4P AC Control (Row ~128+)

**Header Row (Row 128):**
- Col0: NO
- Col7: NC
- Col17: B5
- Col25: F5
- Col31: **M5** ← Price column
- Col36: **N5** ← Price column
- Col44: "4 Pole Contactors"

**Data Rows (129+):**
- Col0: NO count
- Col7: NC count
- Col17: B5 price (e.g., 1845)
- Col25: F5 price (e.g., 1545)
- Col31: M5 price (e.g., 1545)
- Col36: N5 price (e.g., 1845)
- Note: Base SKU column needs verification

**Note:** Need to locate B7, F7, M5WB, N5WB columns - they may be in different columns or section.

### Section 5: LC1E Accessories (Row ~200+)

**Status:** Need to locate and analyze accessory section (expected on "page 10" equivalent).

---

## Column Mapping Summary

### Common Columns (approximate):
- **AC-1 Current**: Various columns (15, 8, etc.)
- **AC-3 Current**: Various columns (23, 21, etc.)
- **HP**: Columns 32, 37
- **kW**: Columns 41, 35, 37
- **NO Aux**: Columns 50, 43, 44, 0
- **NC Aux**: Columns 61, 50, 55, 7
- **Base SKU**: Columns 53, 68 (with asterisks like LC1E120*)

### Price Columns (varies by section):
- **M7 (220V AC)**: Col61 (Section 2)
- **N5 (415V AC)**: Col70 (Section 2), Col36 (Section 4)
- **M5 (220V AC)**: Col76 (Section 2), Col31 (Section 4)
- **BD (24V DC)**: Need to locate
- **B7, F7, M5WB, N5WB**: Need to locate in 4P section

---

## Extraction Challenges

1. **Merged Cells**: Table uses merged cells extensively, making column detection complex
2. **Variable Column Positions**: Column positions vary between sections
3. **Multiple Sections**: LC1E data spans multiple sections with different structures
4. **SKU Format**: Base SKUs appear with asterisks (*, **) that need normalization
5. **Price Columns**: Price columns are not consistently positioned
6. **Aux Contacts**: Represented as "1", "-", or numbers

---

## Recommended Approach

Given the complexity, the extraction script should:

1. **Section Detection**: Identify section boundaries by looking for:
   - "Power Contactors LC1E" headers
   - Frame labels (FRAME-1, FRAME-2, etc.)
   - Coil code headers (M7, N5, BD, etc.)

2. **Column Detection Per Section**: For each section:
   - Locate header row
   - Map column positions dynamically
   - Extract data rows until next section starts

3. **SKU Normalization**: 
   - Extract base reference (LC1E120* → LC1E120)
   - Complete SKU only when price is numeric

4. **Validation**:
   - Verify extracted row counts match expected
   - Check for missing sections
   - Validate price column mappings

---

## Next Steps

1. ✅ Complete structure analysis (in progress)
2. ⚠️ Map all price columns for each section
3. ⚠️ Locate accessory section
4. ⚠️ Customize extraction script with section-specific parsers
5. ⚠️ Test extraction on sample rows
6. ⚠️ Validate extracted data against manual review

