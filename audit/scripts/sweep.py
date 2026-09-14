import os, re, sys, json
from collections import Counter, defaultdict

AUDIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG = os.path.join(os.path.dirname(AUDIT), "ModData", "Data", "Core", "Languages")
PASS = sys.argv[1] if len(sys.argv) > 1 else "pass1"
ENTRY = re.compile(r'<entry\s+name="([^"]*)"\s+value="(.*?)"\s*/>', re.S)
B, E = r"(?<![\w’'ʼ])", r"(?![\w’'ʼ])"
LOW, UP = "а-яіїєґ", "А-ЯІЇЄҐ"
CYR = LOW + UP

RUSSIANISMS = {
	"являтися = бути": r"явля(?:ється|ються|вся|лася|лося|лись|лися|ючись)",
	"являє собою": r"являє собою",
	"приймати участь": r"(?:прийма|прийня)\w* участь",
	"на протязі": r"на протязі",
	"слідуючий": r"слідуюч\w*",
	"получити": r"получ\w*",
	"співпадати": r"співпада\w*",
	"в якості": r"в якості",
	"по відношенню": r"по відношенню",
	"самий + прикметник": r"сам(?:ий|а|е|і|ого|ому|им|их|ої|ій|у|ою) (?:кращ|гірш|більш|менш|сильн|слабк|велик|важлив|перш|останн)\w*",
	"так як": r"так як",
	"у відповідності": r"(?:у|в) відповідності",
	"в залежності": r"(?:у|в) залежності",
	"не дивлячись на": r"не дивлячись на",
	"в кінці кінців": r"в кінці кінців",
	"даний = цей": r"дан(?:ий|а|е|ого|ому|им|их|ої|ій|у|ою)",
	"відмінити = скасувати": r"відмін(?:ити|іть|ено|яти|яє|ив|ила|или|яю)",
	"задавати питання": r"зада\w* питання",
	"приймати міри": r"(?:прийма|прийня)\w* міри",
	"бувший": r"бувш\w+",
	"учбовий": r"учбов\w+",
	"співставити": r"співстав\w+",
	"заключатися": r"заключа\w+",
	"примінити": r"примін\w+",
	"підчас": r"підчас",
	"дієприкметник на -ючий": r"\w*[аяуюіо]юч(?:ий|а|е|і|ого|ому|им|их|ими|ої|ій|у|ою)",
}

BANNED = {
	"Дикунка (canon: Вождиня)": r"Дикунк\w*",
	"Калем (canon: Келем)": r"Калем\w*",
	"Шакалятко (canon: Шакаленя)": r"Шакалят\w*",
	"Кличзлив (canon: Тремтун)": r"Кличзлив\w*",
	"Пустельниця (Anchorite is male)": r"Пустельниц\w*",
	"безодна as an adjective": r"[Бб]езодн(?:а|ий|е|ого|ому|ої|ій|им|их|ими|у|ою)",
}

ALLOW_LATIN = {
	"Steam", "Proxy", "Studios", "Discord", "DLC", "HUD", "FPS", "FXAA", "SMAA", "SSAO",
	"JPG", "PNG", "NumPad", "Shift", "Alt", "Control", "Super", "Tab", "Insert", "Home",
	"End", "Page", "Up", "Down", "Caps", "Lock", "Num", "Print", "Screen", "Pause",
	"Backspace", "Enter", "Esc", "BIOS", "Intel", "Workshop", "AMD", "NVIDIA", "GPU",
	"CPU", "VRAM", "DirectX", "Vulkan", "OpenGL", "Windows", "Linux", "Wayland", "VSync",
	"OK", "IP", "UI", "HDR",
}

TY = r"(?:ти|тебе|тобі|тобою|твій|твоя|твоє|твої|твого|твоєї|твоїх|твоїм|твоєму|твоїми|твою)"
VY = r"(?:ви|вас|вам|вами|ваш|ваша|ваше|ваші|вашого|вашої|ваших|вашим|вашому|вашими|вашу)"
REPEAT = r"(?<![\w’])([^\W\d_]{2,})\s+\1(?![\w’])"


def parse(path):
	if not os.path.exists(path):
		return []
	return ENTRY.findall(open(path, encoding="utf-8-sig").read())


def unescape(v):
	return v.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


# Text with markup and placeholders blanked out
def plain(v):
	return re.sub(r"%\d+%", " ", re.sub(r"<[^>]*>", " ", v))


def snip(text, m):
	return text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")


def numbers(s):
	return sorted(re.findall(r"\d+", re.sub(r"%\d+%", "", re.sub(r"<[^>]*>", "", s))))


# Last meaningful character, ignoring trailing markup, spaces, quotes and brackets
def last_char(s):
	return re.sub(r"(?:<[^>]*>|\s|[«»“”„’)\]*])+$", "", s)[-1:]


findings = []


def add(check, fid, note, frag=""):
	findings.append({"check": check, "id": fid, "note": note, "frag": frag})


entries = []
for f in sorted(os.listdir(os.path.join(LANG, "Ukrainian"))):
	en = dict(parse(os.path.join(LANG, "English", f)))
	for k, v in parse(os.path.join(LANG, "Ukrainian", f)):
		entries.append((f"{f}|{k}", en.get(k, ""), unescape(v)))

terms = defaultdict(lambda: defaultdict(list))
dots = ellipses = 0
for fid, e, u in entries:
	pe, pu = plain(e), plain(u)
	dots += "..." in u
	ellipses += "…" in u

	latin = [
		t for t in re.findall(B + r"[A-Za-z]{2,}" + E, pu)
		if t not in ALLOW_LATIN and not (t == "ZEPHON" and fid == "Messages.xml|DemoEndShared")
	]
	if e and not u.strip():
		add("empty", fid, "Ukrainian value is empty")
	elif latin:
		add("untranslated" if u == e else "latin_words", fid, " ".join(dict.fromkeys(latin)), pu.strip()[:100])

	m = re.search(r"[ыЫэЭъЪёЁ]", pu)
	if m:
		add("russian_letters", fid, m.group(0), snip(pu, m))
	for name, rx in RUSSIANISMS.items():
		m = re.search(B + "(?:" + rx + ")" + E, pu, re.I)
		if m:
			add("russianism", fid, f"{name}: {m.group(0).lower()}", snip(pu, m))
	for name, rx in BANNED.items():
		m = re.search(B + "(?:" + rx + ")" + E, pu)
		if m:
			add("banned_form", fid, name, snip(pu, m))

	if re.search(r"[“”„]", u) and "«" not in u:
		add("quotes", fid, "English-style quotes instead of «»", pu.strip()[:80])
	if u.count("«") != u.count("»"):
		add("quotes", fid, f"unbalanced «» ({u.count('«')} open, {u.count('»')} close)")
	m = re.search(f"[{CYR}]['ʼ`´][{CYR}]", pu)
	if m:
		add("apostrophe", fid, "non-standard apostrophe", snip(pu, m))

	m = re.search(r"[^\s>] {2,}[^\s<]", u)
	if m:
		add("spacing", fid, "double space", snip(u, m))
	m = re.search(f"[{CYR}»)] +[,.;:!?](?!\\.)", pu)
	if m and not re.search(r"\w +[,.;:!?]", pe):
		add("spacing", fid, "space before punctuation", snip(pu, m))
	m = re.search(f"[{LOW}][,;:!?][{CYR}]|[{LOW}]\\.[{UP}]", pu)
	if m:
		add("spacing", fid, "missing space after punctuation", snip(pu, m))
	if e and (e[:1].isspace() != u[:1].isspace() or e[-1:].isspace() != u[-1:].isspace()):
		add("edge_space", fid, "leading or trailing space differs from English", repr(u[:25]) + " ... " + repr(u[-25:]))

	m = re.search(REPEAT, pu, re.I)
	if m and not re.search(REPEAT, pe, re.I):
		add("repeated_word", fid, m.group(1), snip(pu, m))
	if e and numbers(e) != numbers(u):
		add("numbers", fid, f"EN {numbers(e)} vs UK {numbers(u)}")
	m = re.search(r"[^\s\d] - [^\s\d]", pu)
	if m:
		add("dash", fid, "hyphen used as a dash", snip(pu, m))
	m = re.search(r"(?<!\.)\.\.(?!\.)|,,|;;|::|[!?]\.(?!\.)|\.,|,\.", pu)
	if m:
		add("double_punct", fid, m.group(0), snip(pu, m))

	fe, fu = re.search(r"[^\W\d_]", pe), re.search(r"[^\W\d_]", pu)
	if fe and fu and fe.group(0).isupper() != fu.group(0).isupper():
		add("capital", fid, f"EN starts {'upper' if fe.group(0).isupper() else 'lower'}case, UK does not", pu.strip()[:60])
	le, lu = last_char(e), last_char(u)
	if e and ((le in ".!?…" and lu not in ".!?…") or (lu in ".!?" and le not in ".!?…:")):
		add("end_punct", fid, f"EN ends {le!r}, UK ends {lu!r}", u.strip()[-60:])

	if re.search(B + TY + E, pu, re.I) and re.search(B + VY + E, pu, re.I):
		add("register", fid, "ти and ви in one entry")

	if e and len(e) <= 40 and not re.search(r"[<%]", e) and re.search(r"[A-Za-z]", e) and u != e:
		terms[e.strip().rstrip(".").lower()][u.strip().rstrip(".").lower()].append(fid)

for en_term, variants in terms.items():
	if len(variants) > 1:
		ranked = sorted(variants.items(), key=lambda x: -len(x[1]))
		add("term_variants", "TERM|" + en_term, "; ".join(f"{uk} x{len(ids)} ({ids[0]})" for uk, ids in ranked))

path = os.path.join(AUDIT, PASS, "sweep.json")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as fh:
	json.dump(findings, fh, ensure_ascii=False, indent=1)
print(f"{len(entries)} entries scanned, {len(findings)} findings written to {path}")
for check, n in Counter(x["check"] for x in findings).most_common():
	print(f"  {check}: {n}")
print(f"  entries using '...': {dots}, using '…': {ellipses}")
