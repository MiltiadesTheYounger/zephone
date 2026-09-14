import json, os, sys
from collections import Counter

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS, OUT, NAMES = sys.argv[1], sys.argv[2], sys.argv[3:]
base = os.path.join(AUDIT, PASS)
decisions = json.load(open(os.path.join(base, "decisions.json"), encoding="utf-8"))

approved, seen, pending = [], set(), []


def take(fix, source):
	key = (fix["id"], fix["find"])
	if key not in seen:
		seen.add(key)
		approved.append({**fix, "source": source})


for name in NAMES:
	items = json.load(open(os.path.join(base, "findings", name + ".json"), encoding="utf-8"))
	d = decisions.get(name, {})
	for n, item in enumerate(items, 1):
		if n in d.get("pending", []):
			pending.append(f"{name}#{n}")
			continue
		if n in d.get("drop", []):
			continue
		fix = {**item, **d.get("edit", {}).get(str(n), {})}
		if not fix.get("replace") and not fix.get("delete"):
			pending.append(f"{name}#{n} (no replacement)")
			continue
		take(fix, f"{name}#{n}")
	for extra in d.get("add", []):
		take(extra, f"{name}+")

json.dump(approved, open(os.path.join(base, OUT + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

lines = [f"# {OUT}: {len(approved)} fixes", ""]
for sev in ["high", "med", "low"]:
	group = sorted((x for x in approved if x["sev"] == sev), key=lambda x: x["id"])
	if group:
		lines += [f"## {sev} ({len(group)})", ""]
		for x in group:
			lines.append(f"- `{x['id']}` ({x['cat']}): {x['note']}")
			lines.append(f"  - «{x['find']}» → «{x['replace']}»")
		lines.append("")
with open(os.path.join(base, OUT + ".md"), "w", encoding="utf-8", newline="\n") as fh:
	fh.write("\n".join(lines))

print(f"{len(approved)} approved {dict(Counter(x['sev'] for x in approved))}")
print(f"pending: {pending}")
