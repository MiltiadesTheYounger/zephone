import difflib, json, os, re, sys

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UKRAINIAN = os.path.join(os.path.dirname(AUDIT), "ModData", "Data", "Core", "Languages", "Ukrainian")
PASS, NAMES = sys.argv[1], sys.argv[2:]
ENTRY = re.compile(r'<entry\s+name="([^"]*)"\s+value="(.*?)"\s*/>', re.S)
MARKUP = re.compile(r"<[^>]*>|%\d+%|%%")
TOKEN = re.compile(r"<[^>]*>|%\d+%|[\w’'-]+|[^\w\s]")

UK = {}
for f in os.listdir(UKRAINIAN):
	for k, v in ENTRY.findall(open(os.path.join(UKRAINIAN, f), encoding="utf-8-sig").read()):
		UK[f"{f}|{k}"] = v.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

# Word-level diff of each full-entry rewrite, with structural checks
for name in NAMES:
	items = json.load(open(os.path.join(AUDIT, PASS, "findings", name + ".json"), encoding="utf-8"))
	for n, x in enumerate(items, 1):
		if x.get("cat") != "register":
			continue
		old, new = x["find"], x["replace"]
		problems = []
		if UK.get(x["id"]) != old:
			problems.append("find is not the whole current value")
		if sorted(MARKUP.findall(old)) != sorted(MARKUP.findall(new)):
			problems.append("markup or placeholders differ")
		if old.count("«") - old.count("»") != new.count("«") - new.count("»"):
			problems.append("quote balance changed")
		ratio = len(new) / max(1, len(old))
		if not 0.85 <= ratio <= 1.2:
			problems.append(f"length x{ratio:.2f}")
		a, b = TOKEN.findall(old), TOKEN.findall(new)
		changes = [
			f"{' '.join(a[i1:i2]) or '∅'}→{' '.join(b[j1:j2]) or '∅'}"
			for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
			if op != "equal"
		]
		print(f"{name}#{n} [{x['sev']}] {x['id']}{'  !' + '; '.join(problems) if problems else ''}")
		print("   " + " | ".join(changes)[:700])
		if x.get("note"):
			print("   note: " + x["note"][:220])
