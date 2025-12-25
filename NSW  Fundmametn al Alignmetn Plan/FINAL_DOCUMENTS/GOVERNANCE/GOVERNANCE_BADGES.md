# Governance Status Badges

This document provides markdown code for embedding governance status badges in README, dashboard, or other documentation.

---

## 📌 Badge Markdown

### Generic Item Master Status

```markdown
![Generic Item Master](https://img.shields.io/badge/Generic%20Item%20Master-FROZEN-green)
![Generic Item Master](https://img.shields.io/badge/Generic%20Item%20Master-R2__IN__PROGRESS-blue)
![Generic Item Master](https://img.shields.io/badge/Generic%20Item%20Master-R1__PASS-green)
```

### Specific Item Master Status

```markdown
![Specific Item Master](https://img.shields.io/badge/Specific%20Item%20Master-R1__READY-blue)
![Specific Item Master](https://img.shields.io/badge/Specific%20Item%20Master-R0__READY-green)
![Specific Item Master](https://img.shields.io/badge/Specific%20Item%20Master-BLOCKED-red)
```

### CI/Validation Status

```markdown
![Governance Validation](https://img.shields.io/badge/CI--Validation-PASSING-brightgreen)
![Governance Validation](https://img.shields.io/badge/CI--Validation-FAILING-red)
```

---

## 🎨 Badge Color Guide

| Status | Color | Badge Code |
|--------|-------|------------|
| ✅ FROZEN | Green | `green` |
| ✅ PASS/READY | Green | `green` |
| 🔄 IN PROGRESS | Blue | `blue` |
| ⏸️ ON HOLD | Yellow | `yellow` |
| 🚫 BLOCKED | Red | `red` |
| ⚠️ WARNING | Orange | `orange` |

---

## 📝 Example Usage in README

```markdown
# NSW Estimation Software Fundamentals

## Governance Status

![Generic Item Master](https://img.shields.io/badge/Generic%20Item%20Master-FROZEN-green)
![Specific Item Master](https://img.shields.io/badge/Specific%20Item%20Master-R1__READY-blue)
![Governance Validation](https://img.shields.io/badge/CI--Validation-PASSING-brightgreen)

[View Full Dashboard](docs/DASHBOARD_REVIEW_STATUS.md)
```

---

## 🔄 Dynamic Badges (Future Enhancement)

For dynamic badges that update based on actual file status, you can:

1. Use GitHub Actions to generate badge JSON
2. Use shields.io endpoint with custom data
3. Create a badge service that reads governance files

Example GitHub Action workflow:
```yaml
- name: Generate Status Badge
  run: |
    python3 scripts/governance/generate_badge.py
```

---

## 📚 Resources

- [Shields.io](https://shields.io/) - Badge generation service
- [GitHub Actions](https://github.com/features/actions) - CI/CD automation
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) - Documentation framework

---

**Note:** Static badges require manual updates. For automated badges, implement a badge generation script that reads governance file status.

