# Window-A Evidence Header Template

## Purpose
Standard header format for all Window-A evidence files (S1, S2, Gate-0, etc.)

## Template Structure

    === Window-A Evidence Header ===

    Execution Window: Window-A
    Date/Time: <datetime>
    Operator: <operator>
    QuotationId: <QuotationId>
    PanelId: <PanelId>
    TEMPLATE_ID: <TEMPLATE_ID>
    N: <N>
    Stop-Rule Applied: If any Gate fails → STOP → capture evidence → no patching in same window unless explicitly approved.

    ---

## Field Descriptions

- **QuotationId:** The quotation ID used for testing
- **PanelId:** The panel/quotation sale ID used for testing
- **TEMPLATE_ID:** The MasterBomId selected from Gate-0 validation
- **N:** The item count from Gate-0 (must match R1 inserted_count)
- **datetime:** ISO format timestamp (YYYY-MM-DD HH:MM:SS)
- **operator:** Name/identifier of person executing
- **stop-rule line:** Reference to stop rule if execution halted

## Usage Notes

- This header must appear at the top of:
  - `evidence/PHASE2/S1_sql_output.txt`
  - `evidence/PHASE2/S2_sql_output.txt`
  - Any Gate-0 evidence files

- **BOM-GAP-013 Closure Requirement:** TEMPLATE_ID and N must be recorded in evidence header for R1/R2 validation.

- **Gate-0 Mandatory:** Gate-0 SQL output must be captured and TEMPLATE_ID confirmed with N>0 before R1 can start.

## Example

    === Window-A Evidence Header ===

    Execution Window: Window-A
    Date/Time: 2025-01-15 14:30:00
    Operator: Cursor
    QuotationId: 12345
    PanelId: 67890
    TEMPLATE_ID: 42
    N: 15
    Stop-Rule Applied: N/A (all gates passed)

    ---

