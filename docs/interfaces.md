# Where your team talks to the factory

The factory lives in **your data repo** (dbt project or SQL repo) — that's the factory floor. People reach it from four places.

| Who | Where | How | Setup |
|---|---|---|---|
| **Data lead** | Terminal / IDE (Claude Code) | `/data-factory:run …` | install the plugin |
| **Data lead, away from desk** | Claude Code on the web / desktop / phone | same commands on a cloud session of the repo | commit `.claude/settings.json` |
| **Stakeholders** | GitHub issue form | "📊 Data request" → spec comment → approve → PR | 2 files, 10 min |
| **Stakeholders** | Slack | tag `@Claude` in `#data-requests` | Claude Team/Enterprise plan |
| **Nobody (scheduled)** | GitHub Actions | saved spec runs on a cron → PR | 1 file |

---

## 1. Terminal / IDE — the data lead's cockpit
```bash
cd your-data-repo && claude
/plugin install data-factory --marketplace nimrodfisher/data-factory
/data-factory:init
/data-factory:run <request>
```
VS Code and JetBrains work the same way through the Claude Code extension.

## 2. Make the plugin part of the repo (do this once)
Copy [`integrations/claude/settings.json`](../integrations/claude/settings.json) to `.claude/settings.json` in your data repo and commit it. Anyone who opens the repo with Claude Code — including cloud sessions on the web or phone — is offered the Data Factory plugin automatically, with your `.data-factory/` context already there.

## 3. GitHub — the request desk for stakeholders
Two files:
- [`integrations/github/data-request.yml`](../integrations/github/data-request.yml) → `.github/ISSUE_TEMPLATE/data-request.yml`
- [`integrations/github/data-factory.yml`](../integrations/github/data-factory.yml) → `.github/workflows/data-factory.yml`

Then add repo secrets: `ANTHROPIC_API_KEY` and your warehouse credentials **for a dev-only role**. Install the [Claude GitHub app](https://github.com/apps/claude) on the repo.

How it flows — the two gates map to things people already know:
```
Stakeholder opens "📊 Data request"            (asks in plain words + names the decision)
   → factory comments with the SPEC             ← Gate 1: data lead replies "@claude approved, run it"
   → factory builds, inspects, opens a PR       ← Gate 2: data lead reviews & merges
   → ship report is the PR description; stakeholder gets the answer in the issue
```

## 4. Slack — ask where people already are
With a Claude Team or Enterprise plan, Claude can join Slack (Claude Tag) and route coding tasks to Claude Code sessions on your connected repositories.
1. Connect your data repo (with `.claude/settings.json` from step 2 committed).
2. Create `#data-requests`.
3. Pin this message for stakeholders:
   > Tag **@Claude** with your question and the decision it helps with. Start with "Data factory:". Example: *"@Claude Data factory: why did trial-to-paid drop last week? Deciding whether to pause the new onboarding."*
4. The data lead approves specs and merges results in the thread or the linked session.

Availability and setup depend on your plan — see [Claude Code in Slack](https://code.claude.com/docs/en/slack).

## 5. Scheduled — the factory works while you sleep
Copy [`integrations/github/scheduled-recipe.yml`](../integrations/github/scheduled-recipe.yml) → `.github/workflows/weekly-kpi.yml`. It runs `/data-factory:run weekly-kpi-review` every Monday and opens a PR with the results. Duplicate it for `monthly-forecast` or any saved spec.

Locally, without GitHub: `claude -p "/data-factory:run weekly-kpi-review"` from cron does the same.

---

## Security checklist (whatever the interface)
- [ ] The factory's warehouse role can **write only to dev**. Prod is read-only or not granted.
- [ ] Secrets live in your CI/secret store, never in `.data-factory/`.
- [ ] Production changes arrive as PRs; branch protection requires a human review.
- [ ] Decide whether `sealed/` holdouts are committed (traceable) or gitignored (harder to peek at).
