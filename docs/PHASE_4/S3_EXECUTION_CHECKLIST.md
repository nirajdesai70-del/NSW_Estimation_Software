# S3 — Alignment Execution Checklist (Phase‑4, no propagation)
#
# Status: ACTIVE (S3 started)
# Last Updated: 2025-12-18

---

## Scope + Rules (non-negotiable)

- S3 is **alignment only**:
  - ✅ Freeze contract shapes
  - ✅ Map call paths and responsibilities
  - ✅ Resolve ambiguity (who owns what; who calls what)
- S3 is **not propagation**:
  - ❌ No route renames
  - ❌ No behavior changes
  - ❌ No optimization/refactor “for cleanliness”
- Output is **documentation + alignment decisions**, not code movement.

---

## S3 Safe Order (authoritative)

1. **SHARED contract freeze** (CatalogLookup + ReuseSearch)
2. **CIM consumer alignment** to SHARED contracts
3. **BOM alignment** (MBOM / FEED / PBOM apply contracts)
4. **QUO legacy alignment** (consumption + shared-host responsibilities)
5. **QUO‑V2 apply alignment map** (now permitted post‑G4 PASS)

---

## S3 “Done” Gates

S3 is DONE when:

- **Contract shapes are frozen** for SHARED + apply surfaces (MBOM/FEED/PBOM)
- **All consumer call paths are mapped** (no caller ambiguity)
- **No consumer relies on undocumented fields**
- **No route renames** are proposed inside S3 (renames belong to S4 propagation only)
- **No behavior changes** were introduced

---

## Evidence checklist (per document)

- [ ] Endpoint list + ownership recorded
- [ ] Contract request/response shapes recorded (minimum required fields)
- [ ] Consumer map recorded (Legacy QUO, QUO‑V2, CIM, MBOM, FEED, PBOM)
- [ ] Alignment decisions recorded (what remains stable until S4)
- [ ] Explicit “out of scope for S3” section present


