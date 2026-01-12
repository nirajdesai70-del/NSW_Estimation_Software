---
Status: DRAFT
Version: v1.0
Owner: Phase 5 Senate
Last_Updated: 2026-01-27
Scope: Phase-5 Category-D Freeze & Approval Checklist
---

# Category-D Freeze & Approval Checklist

**Purpose:** Provide a formal freeze & sign-off mechanism so Phase-5 artifacts don't drift post-approval.

**Governance:** Post-freeze changes require version bump + Category-D re-approval.

---

## Freeze Scope

The following artifacts are subject to freeze:

- **Category-B APIs** (once finalized)
- **Category-C Schema Canon** (already frozen: v1.0)
- **Phase-3 RAG KB behavior** (tagged: `rag-kb-v1.0-bm25-sha256`)

---

## Required Evidence (Attach)

### Category-C Closure Pack
- [x] Schema Canon v1.0 committed
- [x] DDL/schema.sql committed
- [x] Freeze gate checklist completed
- [x] Tag: `category-c-schema-v1.0` (or equivalent)

**Location:** `docs/PHASE_5/04_SCHEMA_CANON/`

### Category-B API Spec
- [ ] OpenAPI spec finalized (`05_OPENAPI_SKELETON.yaml`)
- [ ] API Surface Map complete (`01_API_SURFACE_MAP.md`)
- [ ] Validation matrix complete (`02_VALIDATION_MATRIX.md`)
- [ ] Error taxonomy finalized (`03_ERROR_TAXONOMY.md`)
- [ ] Versioning policy documented (`04_VERSIONING_POLICY.md`)
- [ ] Examples documented (curl / JSON)
- [ ] Tag: `category-b-api-v1.0` (pending)

**Location:** `docs/PHASE_5/01_CATEGORY_B_API/`

### Validation Parity Matrix
- [ ] API ↔ DB guardrails parity proven
- [ ] All implemented endpoints validated
- [ ] Stubbed endpoints documented (TBD status)

**Location:** `docs/PHASE_5/01_CATEGORY_B_API/02_VALIDATION_MATRIX.md`

### Health Endpoint Snapshot
- [ ] `/health` output confirms expected versions
- [ ] RAG KB `/health` confirms `keyword_backend=bm25`
- [ ] `keyword_docs` non-zero

**Example:**
```json
{
  "status": "ok",
  "keyword_backend": "bm25",
  "kb_version": "v1.0",
  "index_version": "v1.0",
  "keyword_docs": 1234
}
```

### Commit Hashes & Tags
- [ ] Category-C: `{commit_hash}` (tagged)
- [ ] Category-B: `{commit_hash}` (tagged, pending)
- [ ] Phase-3 RAG KB: `{commit_hash}` (tagged: `rag-kb-v1.0-bm25-sha256`)

---

## Approval Checklist

### Scope Confirmation
- [ ] No schema/runtime overlap
- [ ] Category-B consumes Category-C (read-only)
- [ ] Category-B does not modify RAG KB internals
- [ ] All boundaries clearly defined

### Artifacts Committed & Tagged
- [ ] All Category-B documents committed
- [ ] OpenAPI spec committed
- [ ] Validation matrix committed
- [ ] Error taxonomy committed
- [ ] Versioning policy committed
- [ ] Tag created: `category-b-api-v1.0`

### Health Endpoint Verification
- [ ] `/health` reports expected versions
- [ ] RAG KB `/health` reports `keyword_backend=bm25`
- [ ] `keyword_docs` non-zero
- [ ] All services operational

### Error Taxonomy Approved
- [ ] Error codes standardized
- [ ] HTTP status mapping documented
- [ ] Error response format consistent
- [ ] Request ID propagation implemented

### Rollback Path Documented
- [ ] Rollback procedure documented
- [ ] Version downgrade path clear
- [ ] Emergency fix process defined

---

## Sign-Off Roles

### Technical Owner
**Responsibility:** Confirms correctness of API contracts, validation parity, and technical implementation.

**Sign-Off Criteria:**
- [ ] API contracts align with Schema Canon
- [ ] Validation rules mirror DB guardrails
- [ ] Error taxonomy is complete and consistent
- [ ] OpenAPI spec passes lint
- [ ] Examples execute successfully

**Signature:** _________________ Date: _________

---

### Governance Owner
**Responsibility:** Confirms scope & compliance with Phase-5 governance rules.

**Sign-Off Criteria:**
- [ ] No scope bleed from runtime/UI
- [ ] Category-B does not modify Category-C
- [ ] Category-B does not modify RAG KB internals
- [ ] All boundaries respected
- [ ] Freeze rules documented

**Signature:** _________________ Date: _________

---

### Release Owner
**Responsibility:** Authorizes freeze and release of Category-B API v1.0.

**Sign-Off Criteria:**
- [ ] All acceptance gates passed
- [ ] Evidence package complete
- [ ] Health endpoints verified
- [ ] Rollback path documented
- [ ] Ready for client integration

**Signature:** _________________ Date: _________

---

## Post-Freeze Rules

### No-Change Rule
- **No edits without version bump**
- **Any change → new tag + delta note**
- **Emergency fixes require written exception**

### Version Bump Process
1. Create new version branch (e.g., `category-b-api-v1.1`)
2. Document changes in delta note
3. Update version in OpenAPI spec
4. Re-run validation matrix
5. Get Category-D re-approval
6. Tag new version

### Emergency Fix Process
1. Document exception in freeze log
2. Get written approval from Release Owner
3. Apply fix with version bump
4. Update freeze declaration
5. Notify stakeholders

---

## Freeze Declaration Template

```markdown
# Category-D Freeze Declared

**Scope:** Category-B API v1.0  
**Effective Date:** {date}  
**Commit Hash:** {commit_hash}  
**Tag:** `category-b-api-v1.0`

**Frozen Artifacts:**
- OpenAPI spec v1.0
- API Surface Map v1.0
- Validation Matrix v1.0
- Error Taxonomy v1.0
- Versioning Policy v1.0

**Next Change Requires:**
- Formal re-approval
- Version bump
- Category-D sign-off

**Approved By:**
- Technical Owner: {name}, {date}
- Governance Owner: {name}, {date}
- Release Owner: {name}, {date}
```

---

## Freeze Log

| Date | Change | Version | Approved By | Notes |
|------|--------|---------|-------------|-------|
| TBD | Initial freeze | v1.0 | TBD | Category-B completion |

---

## Next Steps

1. Complete Category-B deliverables
2. Gather required evidence
3. Run health endpoint verification
4. Prepare freeze declaration
5. Obtain sign-offs
6. Tag and freeze

---

## References

- Category-B Charter: `../01_CATEGORY_B_API/CATEGORY_B_CHARTER.md`
- Schema Canon: `../04_SCHEMA_CANON/NSW_SCHEMA_CANON_v1.0.md`
- RAG KB: Tag `rag-kb-v1.0-bm25-sha256`
- Phase-5 Governance: `../00_GOVERNANCE/PHASE_5_CHARTER.md`


