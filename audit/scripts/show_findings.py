import json, os, re, sys

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UKRAINIAN = os.path.join(os.path.dirname(AUDIT), "ModData", "Data", "Core", "Languages", "Ukrainian")
PASS, NAMES = sys.argv[1], sys.argv[2:]
ENTRY = re.compile(r'<entry\s+name="([^"]*)"\s+value="(.*?)"\s*/>', re.S)

UK = {}
for f in os.listdir(UKRAINIAN):
	for k, v in ENTRY.findall(open(os.path.join(UKRAINIAN, f), encoding="utf-8-sig").read()):
		UK[f"{f}|{k}"] = v.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

sweep_path = os.path.join(AUDIT, PASS, "findings", "SWEEP.json")
sweep_ids = {x["id"] for x in json.load(open(sweep_path, encoding="utf-8"))} if os.path.exists(sweep_path) else set()


def short(s, n=110):
	s = s.replace("\n", " ")
	return s if len(s) <= n else s[:n] + "…"


for name in NAMES:
	items = json.load(open(os.path.join(AUDIT, PASS, "findings", name + ".json"), encoding="utf-8"))
	rewrites = sum(1 for x in items if x.get("cat") == "register")
	print(f"== {name}: {len(items) - rewrites} findings, {rewrites} register rewrites (see show_diff.py)")
	for n, x in enumerate(items, 1):
		if x.get("cat") == "register":
			continue
		value = UK.get(x["id"])
		count = value.count(x["find"]) if value is not None and x.get("find") else -1
		flags = ([f"find x{count}"] if count != 1 else []) + (["also in SWEEP"] if x["id"] in sweep_ids else [])
		print(f"{n}. [{x['sev']}/{x['cat']}] {x['id']}{'  !' + ', '.join(flags) if flags else ''}")
		print(f"   {short(x['note'], 170)}")
		print(f"   {short(x.get('find', ''))} → {short(x.get('replace', ''))}")
