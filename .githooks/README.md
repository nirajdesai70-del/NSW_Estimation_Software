## Repo-local git hooks

This repository uses **repo-local hooks** stored in `.githooks/`.

### One-time setup

From repo root:

```bash
git config core.hooksPath .githooks
python3 -m pip install --user pre-commit
python3 -m pre_commit run -a
```

### Notes

- Do **not** run `pre-commit install` in this repo (it may refuse when `core.hooksPath` is set).
- Hooks are staged:
  - `.githooks/pre-commit` → `pre_commit --hook-stage pre-commit`
  - `.githooks/commit-msg` → `pre_commit --hook-stage commit-msg`
  - `.githooks/pre-push` → `pre_commit --hook-stage pre-push`

