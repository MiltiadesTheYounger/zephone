import argparse, os, re

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = os.path.join(os.path.dirname(AUDIT), "ModData", "Data", "Core", "Languages")
MAX_CHARS, MAX_ENTRIES, WRAP = 40000, 250, 1500
ENTRY = re.compile(r'<entry\s+name="([^"]*)"\s+value="(.*?)"\s*/>', re.S)
REFERENCE_ONLY = re.compile(r"(?:\s|<[^>]*>|%\d+%|[\d.,:;+\-/()%\[\]])*")

parser = argparse.ArgumentParser()
parser.add_argument("pass_name", nargs="?", default="pass1")
parser.add_argument("--prefix", default="B", help="batch id letter")
parser.add_argument("--start", type=int, default=1, help="first batch number; batches from here on are rebuilt")
parser.add_argument("--exclude", help="file listing File.xml|Key ids to leave out")
parser.add_argument("--only", help="file listing the only File.xml|Key ids to include")
args = parser.parse_args()


def parse(path):
	if not os.path.exists(path):
		return []
	return ENTRY.findall(open(path, encoding="utf-8-sig").read())


def unescape(v):
	return v.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def read_ids(path):
	return {line.strip() for line in open(path, encoding="utf-8") if line.strip()} if path else None


# Break long values after <br/> or a sentence end so no line is too long to read
def wrap(v):
	v = v.replace("\r", "").replace("\n", "\\n")
	lines = []
	for piece in re.split(r"(?<=<br/>)", v):
		while len(piece) > WRAP:
			i = piece.rfind(". ", 0, WRAP)
			cut = i + 2 if i > 0 else WRAP
			lines.append(piece[:cut])
			piece = piece[cut:]
		if piece:
			lines.append(piece)
	return "\n    ".join(lines)


exclude, only = read_ids(args.exclude) or set(), read_ids(args.only)
items, skipped = [], 0
for f in sorted(os.listdir(os.path.join(LANG, "Ukrainian"))):
	en = dict(parse(os.path.join(LANG, "English", f)))
	uk = {k: unescape(v) for k, v in parse(os.path.join(LANG, "Ukrainian", f))}
	for k in [k for k in en if k in uk] + [k for k in uk if k not in en]:
		fid = f"{f}|{k}"
		if fid in exclude or (only is not None and fid not in only):
			continue
		e, u = en.get(k, ""), uk[k]
		if u == e or REFERENCE_ONLY.fullmatch(u):
			skipped += 1
			continue
		items.append((f, k, e, u))

batches, current, size = [], [], 0
for item in items:
	n = len(item[2]) + len(item[3])
	group = (item[0], item[1].split("/")[0])
	if current and (
		size + n > MAX_CHARS
		or len(current) >= MAX_ENTRIES
		or (size > 0.85 * MAX_CHARS and group != (current[-1][0], current[-1][1].split("/")[0]))
	):
		batches.append(current)
		current, size = [], 0
	current.append(item)
	size += n
if current:
	batches.append(current)

out = os.path.join(AUDIT, args.pass_name)
batch_dir = os.path.join(out, "batches")
os.makedirs(batch_dir, exist_ok=True)
os.makedirs(os.path.join(out, "findings"), exist_ok=True)
own = re.compile(re.escape(args.prefix) + r"(\d+)")

for name in os.listdir(batch_dir):
	m = own.fullmatch(name[:-4]) if name.endswith(".txt") else None
	if m and int(m.group(1)) >= args.start:
		os.remove(os.path.join(batch_dir, name))

ledger_path = os.path.join(out, "LEDGER.md")
if os.path.exists(ledger_path):
	ledger = []
	for line in open(ledger_path, encoding="utf-8").read().splitlines():
		m = re.match(r"- \[.\] " + re.escape(args.prefix) + r"(\d+) ", line)
		if not (m and int(m.group(1)) >= args.start):
			ledger.append(line)
else:
	ledger = [f"# Ledger {args.pass_name}", "", "[ ] not scanned, [~] scanned and waiting for triage, [x] triaged and closed", ""]

for i, batch in enumerate(batches, args.start):
	bid = f"{args.prefix}{i:02d}"
	files = list(dict.fromkeys(f for f, _, _, _ in batch))
	chars = sum(len(e) + len(u) for _, _, e, u in batch)
	with open(os.path.join(batch_dir, bid + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
		fh.write(f"# {bid}: {len(batch)} entries from {', '.join(files)}\n\n")
		for f, k, e, u in batch:
			fh.write(f"## {f}|{k}\nEN: {wrap(e)}\nUK: {wrap(u)}\n\n")
	ledger.append(f"- [ ] {bid} | {', '.join(files)} | {len(batch)} entries | {chars:,} chars")

with open(ledger_path, "w", encoding="utf-8", newline="\n") as fh:
	fh.write("\n".join(ledger) + "\n")
print(f"{len(items)} entries in {len(batches)} batches ({args.prefix}{args.start:02d} on), {skipped} identical or reference-only entries skipped")
