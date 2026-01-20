## Contributing

### Repo-local hooks (recommended)

This repo uses repo-local hooks in `.githooks/` (not `.git/hooks/`).

One-time setup after clone:

```bash
git config core.hooksPath .githooks
python3 -m pip install --user pre-commit
python3 -m pre_commit run -a
```

Notes:
- Do **not** run `pre-commit install` here; it may refuse when `core.hooksPath` is set.
- If a commit is blocked due to macOS artifacts (`.DS_Store`, `._*`, `__MACOSX/`), run:

```bash
./tools/cleanup_mac_artifacts.sh .
```

