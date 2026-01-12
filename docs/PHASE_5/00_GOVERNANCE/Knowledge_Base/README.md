# Knowledge Base
## Engineering Decision Documentation

**Purpose:** Capture engineering decisions, rules, and interpretations before they are finalized and moved to working folders.

**Workflow:**
1. **Decision Phase:** Documents are created here for review
2. **Review Phase:** Engineering team reviews and validates
3. **Confirmation Phase:** Once confirmed, documents are transferred to appropriate working folders
4. **Archive Phase:** Original documents remain here as historical record

---

## Folder Structure

```
Knowledge_Base/
├── README.md (this file)
├── INDEX.md (index of all knowledge base documents)
└── [decision_documents].md
```

---

## Current Documents

| Document | Status | Reviewers | Transfer Path | Priority |
|----------|--------|-----------|---------------|----------|
| `SCHNEIDER_FINAL_RULES_v1.2.md` | LOCKED | — | Ready for use | ⭐ PRIMARY |
| `SCHNEIDER_L2_L1_DIFFERENTIATION_CLARIFICATION_v1.0.md` | LOCKED | — | Ready for use | High |
| `SCHNEIDER_L1_L2_EXPANSION_LOGIC_v1.0.md` | LOCKED | — | Ready for use | High |
| `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md` | REVIEW_REQUIRED | Engineering + Procurement | `docs/PHASE_5/ENGINEERING_REVIEW/` or `docs/PHASE_5/INPUT_ASSETS/SCHNEIDER/` | Reference |

---

## Document Status Definitions

- **DRAFT:** Initial creation, not yet ready for review
- **REVIEW_REQUIRED:** Ready for engineering/procurement review
- **UNDER_REVIEW:** Currently being reviewed
- **CONFIRMED:** Review complete, ready for transfer
- **TRANSFERRED:** Moved to working folder (document remains here as archive)

---

## Transfer Rules

1. **No document is deleted** from Knowledge Base after transfer
2. **Transfer date and path** are recorded in document metadata
3. **Working folder version** becomes the active reference
4. **Knowledge Base version** remains as historical record

---

## Review Process

1. Document created in Knowledge Base
2. Status set to `REVIEW_REQUIRED`
3. Reviewers assigned
4. Review comments captured
5. Document updated based on feedback
6. Status changed to `CONFIRMED`
7. Document transferred to working folder
8. Status changed to `TRANSFERRED`

---

## Naming Convention

Format: `[TOPIC]_[DESCRIPTION]_v[VERSION].md`

Examples:
- `SCHNEIDER_CATALOG_INTERPRETATION_RULES_v1.0.md`
- `ABB_VOLTAGE_MAPPING_DECISION_v1.0.md`
- `SIEMENS_ACCESSORY_HANDLING_RULES_v1.0.md`

---

**Last Updated:** 2025-01-XX

