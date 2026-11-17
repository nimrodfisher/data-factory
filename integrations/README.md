# Integrations — copy, paste, done

| File | Copy to (in your data repo) | What it does |
|---|---|---|
| `claude/settings.json` | `.claude/settings.json` | everyone who opens the repo with Claude Code gets the plugin |
| `github/data-request.yml` | `.github/ISSUE_TEMPLATE/data-request.yml` | a "📊 Data request" form for stakeholders |
| `github/data-factory.yml` | `.github/workflows/data-factory.yml` | request → spec comment → `@claude approved, run it` → PR |
| `github/scheduled-recipe.yml` | `.github/workflows/weekly-kpi.yml` | runs a saved spec every Monday → PR |

Step-by-step and the Slack setup: [docs/interfaces.md](../docs/interfaces.md).
