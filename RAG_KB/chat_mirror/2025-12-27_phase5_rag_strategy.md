---
Source: ChatGPT Project Discussion
Date: 2025-12-27
Phase: Phase-5
Status: WORKING
Scope: RAG strategy, KB governance, folder ingestion, chat learning, 360° assistance
Authority: Informational (not canonical until promoted)
---

# Phase 5 RAG Strategy & Implementation Plan

This document captures the complete strategy discussion for implementing a RAG (Retrieval Augmented Generation) system for NSW Estimation Software Phase 5. This conversation establishes the foundation for AI capability that learns continuously from Phase 5 work and provides intelligent assistance.

---

## Context & Objectives

### Primary Goal
Build an AI capability in NSW Estimation that:
1. Starts learning from Phase 5 work immediately
2. Continuously updates a governed knowledge base
3. Provides 360° assistance for NSW Estimation (catalog, L1/L2, rules, pricing, governance)
4. Runs in parallel to Phase 5 development as a sidecar service
5. Stays containerized for fast, reliable responses

### Key Requirements
- RAG should review all Phase 5 work and structure it according to latest canonical format
- RAG should have full access to Phase 5 folder structure but ingest only latest/final files per folder (no junk)
- RAG should learn from ChatGPT conversations via controlled "chat mirror" feed
- RAG should be containerized and scoped to NSW Estimation domain only
- Any new chat must be plugged into RAG automatically

---

## AI Capability Definition

### Three Core AI Outcomes

#### 1. Smart Catalog Assist
- Auto-suggest Item/Category/Subcategory/Attributes/Series/Make from description
- Detect missing fields and propose defaults based on history
- Handle synonyms and common misspellings

#### 2. L1 → L2 Explosion Advisor
- Given L1 intent + features, propose most likely L2 SKU lines
- Handle "one L1 → multiple SKUs" reality
- Manage make/series differences: "built-in vs separate SKU" behavior

#### 3. Price + Risk Intelligence
- Price anomaly flags, duplicates, conflicting SKUs
- Outdated price list detection
- Early-warning KPIs: manual pricing frequency, excessive overrides, discount drift

All three share one core: a continuously updating Knowledge Base (KB).

---

## Knowledge Base Architecture

### Two-Layer Design

#### A) Canonical Relational Truth (Postgres/MySQL)
Structured tables for auditability:
- Items, categories, subcategories, attributes (KVU), make/series policy
- SKU catalog rows + price list versions
- L1 definitions + L2 explosions + mapping rationale
- Overrides, approvals, error corrections

**This stays your "truth".**

#### B) Retrieval Index (Vector/Embedding Store)
AI "memory" layer:
- Item descriptions, SKU descriptions, technical notes
- Past resolved mappings ("when user typed X, we picked Y and it worked")
- Feature-policy explanations and known exceptions

**This becomes your "AI brain", but always references canonical truth.**

**Key Rule**: AI can recommend; only canonical tables can commit.

---

## Learning Signals Capture

Every time a human touches estimation, capture signals automatically:

### Signals to Log (Minimum Viable)
- What user typed (description/intent)
- What AI suggested (top 3 suggestions + confidence)
- What user selected/edited (final choice)
- Why it changed (dropdown reason codes: "wrong make", "separate SKU", "missing attribute", "price mismatch", etc.)
- Result quality proxy:
  - Was it later revised?
  - Was manual pricing used?
  - Was a BOM rebuilt?

**Outcome**: Training dataset without asking anyone to "train AI".

---

## AI Service Architecture

### Sidecar Service with Tight Contract

Don't embed AI logic across screens. Make one AI service with clear endpoints:

#### Core AI APIs (Simple, High ROI)

1. **POST /ai/suggest/item**
   - Input: free text + optional category + context (customer, project, make)
   - Output: ranked matches for Item/L1 + missing fields

2. **POST /ai/suggest/l2**
   - Input: L1 intent + feature selections + make/series
   - Output: candidate SKU lines (with "built-in vs separate" reasoning)

3. **POST /ai/validate**
   - Input: draft quotation/BOM
   - Output: warnings (duplicates, inconsistent attributes, suspicious price, missing dependencies)

4. **POST /ai/explain**
   - Input: any NSW Estimation question
   - Output: answer with citations to exact KB sources and versions

#### Under the Hood (Recommended Approach)
- **RAG (Retrieval Augmented Generation)** for suggestions and reasoning
- **Rules engine always wins** for deterministic constraints
- **AI only fills gaps** and accelerates mapping

This protects you from "AI hallucination" breaking commercial outputs.

---

## KB Update Safety: Human-in-the-Loop + Versioning

### KB Update Workflow
1. AI proposes "New Mapping / New Alias / New SKU relationship"
2. It goes into a Pending KB queue
3. A reviewer (or admin role) approves/rejects
4. Approved entries become:
   - New alias entries
   - Mapping rules
   - Feature-policy exceptions
   - SKU bundling patterns

### Version Everything
- Price list version (already required)
- Catalog snapshot version
- KB version (vector index version + relational mapping version)
- Model prompt/version (even if using hosted model)

This gives you auditability and rollback.

---

## AI-Ready Catalog Fields

While building the catalog XLSX format, add these columns now:

- `Normalized_Name` (cleaned text)
- `Synonyms` (comma-separated, later becomes alias table)
- `Common_Misspellings`
- `Context_Tags` (panel, feeder, accessory, etc.)
- `Bundling_Mode` (Built-in / Optional SKU / Mandatory SKU)
- `Bundling_SKU_List` (if separate)
- `Confidence_Notes` (free text for reviewers)
- `Source` (price list / engineer mapping / project derived)
- `Last_Validated_On` + `Validated_By`

This is what makes AI "learnable".

---

## Implementation Roadmap (Phased)

### Phase A — "AI Telemetry + RAG MVP" (Fastest Value)
- Log signals + build vector index from catalog + past mappings
- Enable suggest/item + validate warnings
- No auto-commit, only suggestions

### Phase B — "Explosion Advisor"
- L1→L2 recommendations based on history + feature-policy
- Add "built-in vs separate SKU" learning

### Phase C — "Continuous Improvement Loop"
- Reviewer queue
- Automated weekly KB refresh
- Offline evaluation: accuracy, override rate, manual pricing reduction

---

## RAG Studying Full Phase 5 Process

### What RAG Should Ingest (High Value)

1. **Phase-5 Docs (Canonical)**
   - NSW_ESTIMATION_MASTER.md, execution plan, rulebook, data model notes
   - Pricing import notes, "Two Truth Layers" governance

2. **Catalog + Price List Artifacts**
   - All normalized catalog XLSX exports
   - Source price list PDFs/XLSX + delta history

3. **Rules Engine Knowledge**
   - Make/Series policy tables
   - L1→L2 explosion rules
   - Bundling rules (built-in vs separate SKU)
   - Attribute KVU rules

4. **Real Usage Telemetry** (as dev starts using it)
   - Suggestions → accepted/rejected
   - Overrides, manual pricing events, error types

5. **Code + Schema Signals** (Read-only)
   - Migration diffs, model changes, seed scripts
   - Rule evaluation code changes

### What NOT to Ingest as "Truth"
- Random chat fragments without "status" tags
- Draft files not marked canonical
- Anything without version/time context

**Critical**: Every knowledge chunk must carry metadata:
- Source
- Version
- EffectiveFrom
- Confidence
- Status (CANONICAL/DRAFT/DEPRECATED)

---

## Smart System Design: RAG + Rules + Review Queue

The smartest system is not pure AI. It's this triangle:

1. **RAG** = Retrieval + Explanation
   - Finds relevant rules/patterns/precedents fast

2. **Rules Engine** = Deterministic Enforcement
   - Validates what is allowed/compatible

3. **Review Queue** = Controlled Learning
   - AI proposes KB updates; humans approve; then it becomes reusable truth

So it gets smarter by learning from approvals and outcomes, not by hallucinating.

---

## Parallel Workstream Design

### Workstream A — "KB Build + Index"
- Build document ingestion pipeline (docs + catalog + policies)
- Create structured "knowledge pack" folder: `docs_phase5/`, `catalog_exports/`, `policies/`, `decisions/`, `price_list_versions/`
- Index into vector store with namespaces

### Workstream B — "AI APIs (Read-Only Assist)"
- `suggest/item`
- `suggest/l2`
- `validate/bom`
- `explain/why` (shows exact references used)

**No write access to production tables.**

### Workstream C — "Telemetry + Offline Evaluation"
- Capture accept/reject signals + override reasons
- Weekly evaluation report:
  - Top failure modes
  - Override rate
  - Manual pricing rate
  - "Unknown mapping" count
- These metrics steer catalog cleanup and rule gaps

### Workstream D — "KB Review PR Workflow"
- AI proposes "new alias / new bundling rule / new mapping exception"
- Auto-creates a KB change record
- Approved changes are merged like code (PR-style)

This becomes a continuous improvement loop that doesn't block core dev.

---

## Practical Governance

### "Two Truth Layers" Enforced in AI
- **Truth Layer 1** (DB + canonical tables): Used for final results
- **Truth Layer 2** (RAG): Used for suggestions + citations

### Version Pinning (Non-Negotiable)

Every AI response must be pinned to:
- CatalogVersion
- PriceListVersion
- PolicyVersion
- KBIndexVersion

So when price lists update, you can re-index and compare.

---

## Folder-Aware Latest-File Ingestion

### Goal
RAG "inherits" the full Phase-5 folder structure but ingests only the latest/final file per folder (no junk).

### Implementation
- **Manifest Builder**: Outputs `00_INDEX.json` (latest-only manifest) + `00_FOLDER_MAP.md` (human-readable map)
- **Latest Selection Rules**:
  - Default: Most recently modified file per folder
  - Override: If folder contains FINAL/CANONICAL marker, prefer that even if older
  - Ignore: Drafts, temp, backup, "_old", "copy", "v0" files (configurable)

### Outputs
1. **Raw Latest Pack (Mirror)**: Exact latest files, copied as-is into KB
2. **Compiled Master (Single Source)**: `01_CANONICAL_MASTER.md` built from latest pack using locked format

So even if Phase-5 is spread across many folders, you still get one "executive truth" file.

---

## Chat Mirror Learning

### Export Rule
Any chat that introduces a decision, structure, or strategy must be saved into `RAG_KB/chat_mirror/` before it is considered known by the project.

### Auto-Ingest Policy
- KB refresh process includes `chat_mirror/` each time
- Authority weighting:
  - Chat mirror defaults to WORKING
  - Only becomes CANONICAL when promoted into `02_DECISIONS_LOG.md` or master file

This achieves "ongoing learning" without corrupting truth.

---

## Storage & Services Planning

### Storage Requirements
- Text docs + manifests: Small (few MB)
- Embeddings/indexes: Hundreds of MB to a few GB depending on chunking and model
- Large PDFs/XLSX exports: Can grow further, but manageable on dev machine if curated

### Services/Addons Worth Planning Now

1. **Vector Store**
   - Lightweight: SQLite-based local index (fastest to start)
   - Scalable: Postgres + pgvector (good governance), or dedicated vector DB if needed later

2. **Object Storage for Snapshots** (Optional)
   - If keeping many catalog versions/price lists: MinIO/S3 bucket for clean version storage

3. **Scheduler/Trigger**
   - Simple `kb_refresh` command initially
   - Later: Filesystem watcher or CI hook to refresh KB on change

4. **RBAC/Access Control** (Recommended)
   - Ensure RAG access is project-scoped (Phase-5 only) and role-limited if multiple users

5. **Evaluation + Regression Suite** (High ROI)
   - Small set of "golden questions" to detect if KB refresh degraded answers
   - Track: precision, override rate, "unknown mapping" rate

6. **Explainability/Citations**
   - Mandatory: Every answer cites file + section + version (prevents hallucination)

7. **UI Mini-Console** (Optional but Useful)
   - "KB status", "last refresh", "delta report", "top gaps", "search"

---

## Containerization for Fast Response

### Recommended Container Split

1. **Indexer Container**
   - Reads repo folders, builds embeddings, updates KB
   - Runs on schedule or file-change triggers

2. **Query Container**
   - Serves interactive answers quickly using already-built KB
   - No heavy indexing at query time

3. **Doc Builder Container**
   - Regenerates `PHASE_5_MASTER_CONSOLIDATED.md` on triggers (daily or on commits)
   - Outputs deterministic artifacts

### Performance Tricks
- Use domain namespaces: `phase5_docs`, `catalog`, `rules`, `scripts`, `trackers`
- Use hybrid retrieval (keyword + vector) so it's fast and precise
- Keep a "hot cache" of:
  - Canonical definitions
  - Locked rules
  - Latest price list version
  - Latest catalog version

That gives speed and prevents wrong context.

---

## Operating Model: Continuous Updates

### Update Cycle Outputs
1. Updated master consolidated file
2. Delta summary (what changed since last build)
3. Risk + gaps list (blocking / high priority / informational)

### Lock Protection
Never overwrites locked content unless:
- Lock status is changed explicitly, OR
- New version section is created (append-only approach)

---

## 360° Assistance (Not Limited to 4 APIs)

Instead of 4 fixed APIs, define capability families inside NSW Estimation:

### Capability Family 1 — Knowledge & Review
- "What changed in Phase-5 since last update?"
- "Show pending items blocking catalog import."
- "Compare rules vs implementation notes."

### Capability Family 2 — Catalog + Pricing Intelligence
- "Find SKUs with missing series/attributes."
- "Identify make-wise bundling patterns (built-in vs separate SKU)."
- "Spot duplicates / conflicting SKU mappings."

### Capability Family 3 — Rule Engine & L1→L2 Behavior
- "Given this L1 intent + features, what L2 lines should appear?"
- "Which policy rule triggered this SKU split?"

### Capability Family 4 — Governance/Traceability
- "Is this decision already locked? Where?"
- "Create a change log entry for this modification."

So it's "360°", but still strictly inside NSW Estimation.

---

## Three Categories of Project Folder Access

RAG needs full access to all three categories:

1. **CANONICAL_DOCS**
   - `docs/` + "LOCKED/CANONICAL" planning documents
   - Phase-5 master, execution plan, rulebook

2. **IMPLEMENTATION_ARTIFACTS**
   - Scripts, migrations, seed scripts, converters
   - Cursor outputs

3. **INPUTS_AND_SNAPSHOTS**
   - Price lists, catalog exports, mapping tables
   - Sample files, tracker sheets (or their exported CSV/MD summaries)

All three are gathered into KB "namespaces" inside `/RAG_KB/` so RAG effectively has full access—but through a controlled gateway.

---

## 5R Summary

### Results
- RAG becomes a "Phase-5 memory" that learns from docs, catalog, policies, and real estimation behavior
- Runs alongside development with minimal coupling, improving accuracy over time
- Provides 360° support for NSW Estimation while staying containerized and fast

### Risks
- KB contamination (draft/old rules mixed with canonical)
- AI "overreach" if allowed to write to core tables
- Version drift when price lists update frequently
- Wrong "latest" selection if naming/version markers aren't standardized
- Chat content polluting truth if not authority-gated
- Index bloat if PDFs/XLSX versions are ingested without curation

### Rules
- AI is assist-only (suggest/validate/explain), not commit
- Mandatory metadata + status tags on every ingested artifact
- All suggestions must cite exact KB sources and versions
- RAG indexes only `/RAG_KB/` (curated gateway)
- Chat mirror is WORKING unless promoted to CANONICAL
- Locked sections are immutable; updates go into new version blocks
- Query container is read-only to canonical DB; writes only via PR/review workflow
- Phase-5 namespace only (no external/general knowledge)

### Roadmap
1. Bootstrap Knowledge Pack + first master consolidation
2. Build indexer + query + doc-builder containers
3. Enable "Phase-5 Master Consolidation" auto-build + delta report
4. Add gap/risk scoring + regression questions library
5. Add telemetry once Phase-5 UI/dev usage begins

### References
- NSW v1.3 model principles (L1 intent + L2 SKU pricing, KVU attributes, make/series policy)
- Phase-5 governance approach (entry gates, locked rules, two-truth layers)
- Phase 5 goal: stable rule engine + repeatable price list import + future-proof AI layer
- Catalog + L1/L2 + make/series policy framework already established in Phase-5 discussions

---

## Next Actions

1. **Upload this conversation** to Phase 5 via Cursor ✓
2. **Create RAG_KB folder structure** with rulebook
3. **Run first KB refresh** to compile Phase 5 work till now
4. **Review compiled master** and promote final rules
5. **Build RAG runtime containers** (indexer/query/doc-builder)

---

**Status**: WORKING — This conversation establishes the strategy. Final governance rules will be promoted to CANONICAL after review and integration into Phase 5 master documents.

