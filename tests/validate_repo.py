"""Structural checks for the plugin: manifests, frontmatter, routers, links. Run: python3 tests/validate_repo.py"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(ROOT, "plugins", "data-factory")
errors = []


def frontmatter(path):
    text = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"missing frontmatter: {os.path.relpath(path, ROOT)}")
        return {}
    return dict(re.findall(r"^(\w[\w-]*):\s*(.+)$", m.group(1), re.M))


market = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
for p in market["plugins"]:
    src = os.path.normpath(os.path.join(ROOT, p["source"]))
    manifest = os.path.join(src, ".claude-plugin", "plugin.json")
    if not os.path.exists(manifest):
        errors.append(f"plugin source without plugin.json: {p['source']}")
    elif json.load(open(manifest))["name"] != p["name"]:
        errors.append("plugin name mismatch between marketplace.json and plugin.json")
json.load(open(os.path.join(PLUGIN, "hooks", "hooks.json")))

for f in sorted(os.listdir(os.path.join(PLUGIN, "agents"))):
    fm = frontmatter(os.path.join(PLUGIN, "agents", f))
    for key in ("name", "description", "tools"):
        if key not in fm:
            errors.append(f"agents/{f}: missing {key}")
    if fm.get("name") and fm["name"] != f[:-3]:
        errors.append(f"agents/{f}: name '{fm['name']}' != filename")

for f in sorted(os.listdir(os.path.join(PLUGIN, "commands"))):
    if "description" not in frontmatter(os.path.join(PLUGIN, "commands", f)):
        errors.append(f"commands/{f}: missing description")

skills_dir = os.path.join(PLUGIN, "skills")
all_refs = {r for s in os.listdir(skills_dir) for r in os.listdir(os.path.join(skills_dir, s, "references"))}
all_refs |= set(os.listdir(os.path.join(skills_dir, "factory-playbook", "templates")))
all_refs |= set(os.listdir(os.path.join(skills_dir, "factory-playbook", "recipes")))
for s in sorted(os.listdir(skills_dir)):
    fm = frontmatter(os.path.join(skills_dir, s, "SKILL.md"))
    if fm.get("name") != s:
        errors.append(f"skills/{s}: frontmatter name must equal folder name")
    if len(fm.get("description", "")) > 1024:
        errors.append(f"skills/{s}: description > 1024 chars")
    refs = os.path.join(skills_dir, s, "references")
    router = open(os.path.join(refs, "router.md")).read()
    for ref in os.listdir(refs):
        if ref != "router.md" and f"`{ref}`" not in router:
            errors.append(f"skills/{s}: {ref} not referenced in router.md")
    for linked in re.findall(r"`([\w-]+\.md)`", router):
        if linked not in all_refs:
            errors.append(f"skills/{s}: router points to missing {linked}")

# relative markdown links resolve
for dirpath, _, files in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(dirpath, f)
            for link in re.findall(r"\]\(([^)#\s]+)\)", open(path).read()):
                if not link.startswith(("http", "mailto")) and not os.path.exists(os.path.normpath(os.path.join(dirpath, link))):
                    errors.append(f"broken link in {os.path.relpath(path, ROOT)}: {link}")

if errors:
    print("\n".join("❌ " + e for e in errors))
    sys.exit(1)
n_agents = len(os.listdir(os.path.join(PLUGIN, "agents")))
n_refs = sum(len(os.listdir(os.path.join(skills_dir, s, "references"))) for s in os.listdir(skills_dir))
print(f"✅ plugin valid — {n_agents} agents, {len(os.listdir(os.path.join(PLUGIN, 'commands')))} commands, "
      f"{len(os.listdir(skills_dir))} skills, {n_refs} reference files")
