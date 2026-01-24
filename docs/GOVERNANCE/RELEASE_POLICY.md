# Release & Tag Policy (SemVer)

**Scope:** NSW_Estimation_Software
**Owner:** @nirajdesai70-del • **Change approver:** Code owners

## Versioning
- **SemVer**: `MAJOR.MINOR.PATCH`
- **Tags**: `vX.Y.Z` (annotated)

## Release Types
- **PATCH**: bug fix / docs only / test-only; no behavior change.
- **MINOR**: backward-compatible features; no protected behavior change.
- **MAJOR**: breaking change (requires G4/G5 gates + migration notes).

## Gates (must pass before tagging)
- Required checks (security + quality) green on PR.
- Code-owner approval present.
- Conversation resolution satisfied.

## Changelog
- Source of truth: PR titles (Conventional Commits).
- On tag: generate `CHANGELOG.md` section from merged PRs since last tag.

## Tagging Steps (maintainer)
1) Merge PR(s) to `main`.
2) Prepare release notes (PR titles grouped by type).
3) Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"` → `git push origin vX.Y.Z`.
4) Create GitHub Release with notes.

## Rollback
- Revert via PR; record in Control Tower.
