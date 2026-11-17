# Using Data Factory with other agent tools

Data Factory is a Claude Code plugin, but its knowledge and roles are plain markdown.

| Piece | Path | Portable? |
|---|---|---|
| Knowledge skills | `plugins/data-factory/skills/*/` | ✅ Agent Skills format (`SKILL.md` + references) — usable by tools that read skills, or paste the reference files as context |
| Station roles | `plugins/data-factory/agents/*.md` | ✅ use the body as a system prompt / custom mode / sub-agent definition |
| Operating playbook & templates | `plugins/data-factory/skills/factory-playbook/` | ✅ follow it manually or from your tool's orchestration |
| Commands (`/data-factory:*`) | `plugins/data-factory/commands/` | ⚠️ Claude Code slash commands; elsewhere, paste the body as the prompt |
| Safety interlock | `plugins/data-factory/scripts/sql_guard.py` | ⚠️ Claude Code hook; elsewhere, wire it into your tool's pre-command hook if it has one |

## If you are an AI agent reading this repo
To act as the Factory Manager: read `plugins/data-factory/commands/run.md`, then `plugins/data-factory/skills/factory-playbook/SKILL.md` and its router. Project state lives in `.data-factory/`. Never write to the schema named in `environments.prod`, and never let builder roles read `runs/*/sealed/`.
