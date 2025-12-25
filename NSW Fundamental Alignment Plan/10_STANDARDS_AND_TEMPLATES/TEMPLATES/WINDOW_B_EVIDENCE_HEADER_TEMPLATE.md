# Window-B Evidence Header Template

## Purpose
Standard header format for all Window-B evidence files (Phase-3 node history, restore, Phase-4 lookup integrity)

## Template Structure

    === Window-B Evidence Header ===

    Execution Window: Window-B
    Date/Time: <datetime>
    Operator: <operator>
    QuotationId: <QuotationId>
    Target Node IDs: <target node ids>
    Restore Timestamp: <restore timestamp> (Phase-3 restore only)
    Stop-Rule Applied: If any Gate fails → STOP → capture evidence → no patching in same window unless explicitly approved.

    ---

## Field Descriptions

- **QuotationId:** The quotation ID used for testing
- **Target Node IDs:** Comma-separated list of QuotationSaleBomId values used for verification
- **Restore Timestamp:** ISO format timestamp (YYYY-MM-DD HH:MM:SS) for point-in-time restore testing (Phase-3 restore only)
- **datetime:** ISO format timestamp (YYYY-MM-DD HH:MM:SS)
- **operator:** Name/identifier of person executing
- **stop-rule line:** Reference to stop rule if execution halted

## Usage Notes

- This header must appear at the top of:
  - `evidence/PHASE3/node_history_output.txt` (Phase-3 Gate-3: Node History Verification)
  - `evidence/PHASE3/restore_output.txt` (Phase-3 Gate-3: Restore Verification)
  - `evidence/PHASE4/lookup_integrity_output.txt` (Phase-4 Gate-3: Lookup Integrity Verification)

- **Phase-3 Gate-2 Requirement:** Implementation Window must complete before Gate-3 verification can begin.

- **Phase-3 Gate-3 Requirement:** Both node history and restore verification must pass.

- **Phase-4 Gate-3 Requirement:** All lookup pipeline integrity checks must pass.
