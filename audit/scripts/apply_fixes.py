import json, os, re, sys

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UKRAINIAN = os.path.join(os.path.dirname(AUDIT), "ModData", "Data", "Core", "Languages", "Ukrainian")
ENTRY = r'(<entry\s+name="{}"\s+value=")(.*?)("\s*/>)'


# Ukrainian files store markup escaped; bare & first, existing entities kept
def escape(v):
	v = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+);)", "&amp;", v)
	return v.replace("<", "&lt;").replace(">", "&gt;")


DRY_RUN = "--dry-run" in sys.argv
fixes = json.load(open(next(a for a in sys.argv[1:] if a != "--dry-run"), encoding="utf-8"))
by_file = {}
for fix in fixes:
	f, k = fix["id"].split("|", 1)
	by_file.setdefault(f, []).append((k, fix))

applied, problems = 0, []
for f, items in by_file.items():
	path = os.path.join(UKRAINIAN, f)
	if open(path, "rb").read(3) != b"\xef\xbb\xbf":
		sys.exit(f"{f}: missing BOM, refusing to write")
	text = open(path, encoding="utf-8-sig", newline="").read()
	for k, fix in items:
		m = re.search(ENTRY.format(re.escape(k)), text, re.S)
		if not m:
			problems.append(f"{fix['id']}: key not found")
			continue
		if not fix.get("replace") and not fix.get("delete"):
			problems.append(f"{fix['id']}: no replacement given")
			continue
		value, find, replace = m.group(2), escape(fix["find"]), escape(fix.get("replace", ""))
		count = value.count(find)
		if fix.get("all") and count:
			text = text[:m.start(2)] + value.replace(find, replace) + text[m.end(2):]
			applied += 1
			continue
		if count != 1:
			state = "already applied" if count == 0 and replace and replace in value else f"find text occurs {count} times"
			problems.append(f"{fix['id']}: {state}")
			continue
		text = text[:m.start(2)] + value.replace(find, replace) + text[m.end(2):]
		applied += 1
	if not DRY_RUN:
		open(path, "w", encoding="utf-8-sig", newline="").write(text)

print(f"{'would apply' if DRY_RUN else 'applied'} {applied} of {len(fixes)}")
for p in problems:
	print("  " + p)
