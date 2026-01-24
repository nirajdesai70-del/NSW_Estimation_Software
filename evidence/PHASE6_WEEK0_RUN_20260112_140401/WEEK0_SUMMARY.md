# PHASE-6 | WEEK-0 — Evidence Summary

**Run ID:** PHASE6_WEEK0_RUN_20260112_140401  
**Timestamp:** 2026-01-12 14:04:04  
**Runner:** scripts/run_week0_checks.sh  
**Backend Health URL:** http://localhost:8003/health

---

## Result

**STATUS:** ✅ PASS (Week-0 verification completed)

> Note: Week-0 is read-only. This runner does not change schema, data, or code.

---

## Evidence Index (Files)

- backend_health.txt
- tool_versions.txt
- ports_snapshot.txt
- git_status.txt (if git available)
- git_head.txt (if git available)
- git_branch.txt (if git available)
- git_diffstat.txt (if git available)
- optional_status_dev.txt (if present)
- optional_smoke_dev.txt (if present)
- P6_ENTRY_001_ENV_SANITY.md


## Backend Health Output

{"status":"healthy","service":"nsw-api"}
## Tool Versions

Timestamp: 2026-01-12 14:04:02
OS: Darwin Nirajs-MacBook-Pro.local 25.1.0 Darwin Kernel Version 25.1.0: Mon Oct 20 19:26:04 PDT 2025; root:xnu-12377.41.6~2/RELEASE_ARM64_T8122 arm64

Bash: 3.2.57(1)-release

Python: python not found
Pip: pip 25.3 from /Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/pip (python 3.13)

Node: v25.2.1
NPM: npm not found

Docker: Docker version 29.1.3, build f52814d
Docker Compose: Docker Compose version v2.40.3-desktop.1

## Ports Snapshot

Timestamp: 2026-01-12 14:04:04
Ports (hint): 8003,8000,8011

== lsof (listeners) ==
COMMAND     PID       USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe   900 nirajdesai    9u  IPv4 0x4ae76cec5f45d418      0t0  TCP *:7000 (LISTEN)
ControlCe   900 nirajdesai   10u  IPv6 0x65347b95cb03a255      0t0  TCP *:7000 (LISTEN)
ControlCe   900 nirajdesai   11u  IPv4 0xed4f2f3e1de1ff02      0t0  TCP *:5000 (LISTEN)
ControlCe   900 nirajdesai   12u  IPv6 0x212a543cad5703ad      0t0  TCP *:5000 (LISTEN)
rapportd    909 nirajdesai   10u  IPv4 0xc37883ed09c80d0a      0t0  TCP *:60362 (LISTEN)
rapportd    909 nirajdesai   11u  IPv6 0x850b2d9c09c75489      0t0  TCP *:60362 (LISTEN)
postgres   1061 nirajdesai    7u  IPv6 0x7501ed101f29a4b9      0t0  TCP [::1]:5432 (LISTEN)
postgres   1061 nirajdesai    8u  IPv4 0xe20a8fa645cea717      0t0  TCP 127.0.0.1:5432 (LISTEN)
Google     1122 nirajdesai   43u  IPv6 0x2279d0b4097630f9      0t0  TCP [::1]:7679 (LISTEN)
AdobeReso  1758 nirajdesai   10u  IPv4 0xe97dd6cf6915a77d      0t0  TCP 127.0.0.1:19292 (LISTEN)
com.docke  2379 nirajdesai  155u  IPv6 0x9d945f3251ed7e3c      0t0  TCP *:8011 (LISTEN)
com.docke  2379 nirajdesai  164u  IPv6 0x670ac22f18adec1a      0t0  TCP *:5433 (LISTEN)
Python    10655 nirajdesai    5u  IPv4 0x3cfacd52eb720d27      0t0  TCP *:8003 (LISTEN)
node      43423 nirajdesai   16u  IPv4 0x63b75d31d9de5f3d      0t0  TCP *:3000 (LISTEN)
php       89060 nirajdesai    6u  IPv4 0xc98fd258d598b062      0t0  TCP 127.0.0.1:8000 (LISTEN)
Python    93115 nirajdesai    5u  IPv4 0x3cfacd52eb720d27      0t0  TCP *:8003 (LISTEN)

## Git Branch

### Git Branch
$ git rev-parse --abbrev-ref HEAD

feat/rag-connections-upgrade


## Git HEAD

### Git HEAD
$ git rev-parse HEAD

1ed06e91c9863c9b7ec0167dd3aafcf2f4c272bb


## Git Status (Porcelain)

### Git Status
$ git status --porcelain=v1

warning: could not open directory 'NSW Fundamental Alignment Plan/ARCHIVE/': Operation not permitted
warning: could not open directory 'tools/catalog_pipeline/output/archive/': Operation not permitted
warning: could not open directory 'tools/catalog_pipeline_v2/ARCH_EXECUTION/2026-01-03_PHASE5_CLEANUP_20260103_164434/docs/': Operation not permitted
warning: could not open directory 'ARCHIVE/': Operation not permitted
warning: could not open directory 'RAG_KB/': Operation not permitted
warning: could not open directory 'docs/': Operation not permitted
 M .github/workflows/rag_ci.yml
 M .gitignore
 M README.md
 M backend/app/api/v1/endpoints/quotation.py
 M backend/app/core/database.py
 M backend/app/core/exceptions.py
 M backend/app/main.py
 M docker-compose.yml
 M docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md
 M docs/PHASE_5/01_CATEGORY_B_API/04_VERSIONING_POLICY.md
 M docs/PHASE_5/01_CATEGORY_B_API/CATEGORY_B_CHARTER.md
 M docs/PHASE_5/02_CATEGORY_D_FREEZE/CATEGORY_D_FREEZE_CHECKLIST.md
 M evidence/PHASE6_WEEK4_EVIDENCE_PACK.md
 M frontend/src/App.tsx
 M frontend/src/components/Layout.tsx
 M frontend/src/pages/Home.tsx
 M frontend/src/services/api.ts
 M frontend/vite.config.ts
?? ._NEPL_V2_QUOTATION_FEATURES_COVERAGE.md
?? ._PHASE6_COMPREHENSIVE_VERIFICATION_REPORT.md
?? ._PHASE6_COMPREHENSIVE_WEEK_REVIEW.md
?? ._PHASE6_DOCUMENT_REVIEW_MATRIX.md
?? ._PHASE6_DOCUMENT_REVIEW_MATRIX_W0_W4_ONLY.md
?? ._PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md
?? ._PHASE6_EXECUTION_ORDER_REVIEW_AND_RECOMMENDATIONS.md
?? ._PHASE6_MATRIX_VERIFICATION_CHECKLIST.md
?? ._PHASE6_MATRIX_VERIFICATION_COMPLETE.md
?? ._PHASE6_MATRIX_VERIFICATION_RESULTS.md
?? ._PHASE6_PROGRESS_SUMMARY.md
?? ._PHASE6_WEEK0_DETAILED_PLAN.md
?? ._PHASE6_WEEK0_EVIDENCE_PACK.md
?? ._PHASE6_WEEK0_TO_WEEK4_AUDIT.md
?? ._PHASE6_WEEK10_DETAILED_PLAN.md
?? ._PHASE6_WEEK11_DETAILED_PLAN.md
?? ._PHASE6_WEEK12_DETAILED_PLAN.md
?? ._PHASE6_WEEK1_DETAILED_PLAN.md
?? ._PHASE6_WEEK2_DETAILED_PLAN.md
?? ._PHASE6_WEEK3_DETAILED_PLAN.md
?? ._PHASE6_WEEK4_DETAILED_PLAN.md
?? ._PHASE6_WEEK5_DETAILED_PLAN.md
?? ._PHASE6_WEEK6_DETAILED_PLAN.md
?? ._PHASE6_WEEK7_DETAILED_PLAN.md
?? ._PHASE6_WEEK8_5_DETAILED_PLAN.md
?? ._PHASE6_WEEK8_DETAILED_PLAN.md
?? ._PHASE6_WEEK9_DETAILED_PLAN.md
?? ._PHASE_6_COMPLETE_SCOPE_AND_TASKS.md
?? ._PHASE_6_CORRECTED_PLAN_SUMMARY.md
?? ._PHASE_6_EXECUTION_PLAN.md
?? ._PHASE_6_LEGACY_PARITY_ADDITION.md
?? ._PHASE_6_LEGACY_PARITY_CHECKLIST.md
?? ._PHASE_6_REVISION_SUMMARY.md
?? ._START_NSW_API.sh
?? ._WEEK6_CODE_REVIEW_FIXES.md
?? ._WEEK6_STATUS.md
?? ._WHY_NEPL_FEATURES_NOT_VISIBLE.md
?? ._logs
?? .cursorignore
?? .githooks/
?? FIX_PORT_8003.md
?? NEPL_V2_QUOTATION_FEATURES_COVERAGE.md
?? PHASE6_COMPREHENSIVE_VERIFICATION_REPORT.md
?? PHASE6_COMPREHENSIVE_WEEK_REVIEW.md
?? PHASE6_DOCUMENT_REVIEW_MATRIX.md
?? PHASE6_DOCUMENT_REVIEW_MATRIX_W0_W4_ONLY.md
?? PHASE6_EXECUTION_ORDER_AND_START_CHECKLIST.md
?? PHASE6_EXECUTION_ORDER_REVIEW_AND_RECOMMENDATIONS.md
?? PHASE6_MATRIX_VERIFICATION_CHECKLIST.md
?? PHASE6_MATRIX_VERIFICATION_COMPLETE.md
?? PHASE6_MATRIX_VERIFICATION_RESULTS.md
?? PHASE6_PROGRESS_SUMMARY.md
?? PHASE6_WEEK0_DETAILED_PLAN.md
?? PHASE6_WEEK0_EVIDENCE_PACK.md
?? PHASE6_WEEK0_TO_WEEK4_AUDIT.md
?? PHASE6_WEEK10_DETAILED_PLAN.md
?? PHASE6_WEEK11_DETAILED_PLAN.md
?? PHASE6_WEEK12_DETAILED_PLAN.md
?? PHASE6_WEEK1_DETAILED_PLAN.md
?? PHASE6_WEEK2_DETAILED_PLAN.md
?? PHASE6_WEEK3_DETAILED_PLAN.md
?? PHASE6_WEEK4_DETAILED_PLAN.md
?? PHASE6_WEEK5_DETAILED_PLAN.md
?? PHASE6_WEEK6_DETAILED_PLAN.md
?? PHASE6_WEEK7_DETAILED_PLAN.md
?? PHASE6_WEEK8_5_DETAILED_PLAN.md
?? PHASE6_WEEK8_DETAILED_PLAN.md
?? PHASE6_WEEK9_DETAILED_PLAN.md
?? PHASE_6_COMPLETE_SCOPE_AND_TASKS.md
?? PHASE_6_CORRECTED_PLAN_SUMMARY.md
?? PHASE_6_EXECUTION_PLAN.md
?? PHASE_6_LEGACY_PARITY_ADDITION.md
?? PHASE_6_LEGACY_PARITY_CHECKLIST.md
?? PHASE_6_REVISION_SUMMARY.md
?? QUICK_SMOKE_TEST.sh
?? SMOKE_TEST_INSTRUCTIONS.md
?? START_NSW_API.sh
?? WEEK6_CODE_REVIEW_FIXES.md
?? WEEK6_STATUS.md
?? WHY_NEPL_FEATURES_NOT_VISIBLE.md
?? backend/app/api/v1/endpoints/._quotation.py
?? backend/app/api/v1/endpoints/discounts.py
?? backend/app/api/v1/endpoints/tax.py
?? backend/app/api/v1/schemas/._bom_items_read.py
?? backend/app/api/v1/schemas/._error_summary.py
?? backend/app/api/v1/schemas/bom_items_read.py
?? backend/app/api/v1/schemas/cost_adders.py
?? backend/app/api/v1/schemas/error_summary.py
?? backend/app/api/v1/schemas/quotation_copy.py
?? backend/app/api/v1/schemas/quotation_read.py
?? backend/app/api/v1/schemas/quotation_structure_read.py
?? backend/app/services/._error_warning_service.py
?? backend/app/services/._user_friendly_messages.py
?? backend/app/services/__init__.py
?? backend/app/services/bom_service.py
?? backend/app/services/cost_adder_service.py
?? backend/app/services/error_warning_service.py
?? backend/app/services/user_friendly_messages.py
?? backend/app/validators/costing_view_rules.py
?? backend/scripts/RUN_SMOKE_TESTS.md
?? backend/scripts/setup_postgres_env.sh
?? evidence/._PHASE6_WEEK0_RUN_20260112_140401
?? evidence/._PHASE6_WEEK4_EVIDENCE_PACK.md
?? evidence/._PHASE6_WEEK6_EVIDENCE_PACK.md
?? evidence/PHASE6_WEEK0_RUN_20260112_140401/
?? evidence/PHASE6_WEEK6_EVIDENCE_PACK.md
?? frontend/._.env
?? frontend/._.env.example
?? frontend/._package-lock.json
?? frontend/._vite.config.ts
?? frontend/.env.example
?? frontend/DAY5_COMPLETION_SUMMARY.md
?? frontend/DAY5_NAVIGATION_ROUTES.md
?? frontend/package-lock.json
?? frontend/src/._api
?? frontend/src/api/
?? frontend/src/pages/._Home.tsx
?? frontend/src/pages/FeederBOM.tsx
?? frontend/src/pages/PanelFeeders.tsx
?? frontend/src/pages/QuotationDetail.tsx
?? frontend/src/pages/QuotationList.tsx
?? frontend/src/services/._api.ts
?? project/nish/NISH_SYSTEM_REFERENCE.md
?? project/nish/PHASE_6_NISH_REVIEW_REPORT.md
?? scripts/._README_DEV.md
?? scripts/._run_phase6_master.sh
?? scripts/._run_week0_checks.sh
?? scripts/._run_week6_checks.sh
?? scripts/._smoke_dev.sh
?? scripts/._start_all_dev.sh
?? scripts/._status_dev.sh
?? scripts/._stop_all_dev.sh
?? scripts/README_DEV.md
?? scripts/check_schema_drift.sh
?? scripts/run_phase6_master.sh
?? scripts/run_reuse_tests.sh
?? scripts/run_week0_checks.sh
?? scripts/run_week3_checks.sh
?? scripts/run_week6_checks.sh
?? scripts/smoke_dev.sh
?? scripts/start_all_dev.sh
?? scripts/status_dev.sh
?? scripts/stop_all_dev.sh
?? tests/._errors
?? tests/catalog/
?? tests/costing/
?? tests/errors/
?? tests/quotation/.___pycache__
?? tests/reuse/
?? tests/summary/.___pycache__
?? tools/clean_os_junk.sh


## Git Diffstat

### Git Diffstat (working tree)
$ git diff --stat

error: open("docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md"): Operation not permitted
fatal: cannot hash docs/PHASE_5/00_GOVERNANCE/PHASE_5_DECISIONS_REGISTER.md

