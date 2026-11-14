"""Fill the measured sections of an ad spec from its source text.

Usage: python3 build_spec.py <source.txt> <spec_template.md> <out.md>

The template may contain these placeholders, each replaced with a markdown block
computed from the source (every non-empty line = one paragraph):
  {{INDEX}}      paragraph index table (¶ | first 6 words | words | sentences | beat)
  {{BASELINE}}   Step 1C baseline measurements
  {{LINE}}       Step 5 counted line-level items (punctuation, caps, questions, numbers, you-density)
  {{RHYTHM}}     Step 4F rhythm map by tenths
  {{BEATWORDS}}  words and % per beat, checks every ¶ is assigned once
Beats are read from the template's first line of the form:
  <!-- BEATS: 1-6:Cold open | 7-10:Grief objects | ... -->
"""
import re
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from measure import paragraphs, sentences, syllables, words  # noqa: E402


def pos(pw, i, total):
    return f"{sum(pw[:i]) / total:.0%}"


def main():
    src, tpl, out = sys.argv[1:4]
    paras = paragraphs(src)
    pw = [len(words(p)) for p in paras]
    ps = [sentences(p) for p in paras]
    total = sum(pw)
    n = len(paras)
    t = open(tpl, encoding="utf-8").read()

    m = re.search(r"<!-- BEATS: (.*?) -->", t)
    beats = []
    if m:
        for part in m.group(1).split("|"):
            rng, label = part.strip().split(":", 1)
            a, z = (int(x) for x in rng.split("-"))
            beats.append((a, z, label.strip()))
    beat_of = {}
    for b, (a, z, label) in enumerate(beats, 1):
        for k in range(a, z + 1):
            beat_of.setdefault(k, []).append(b)

    # INDEX
    rows = ["| ¶ | First 6 words (verbatim) | Words | Sentences | Beat |", "|---|---|---|---|---|"]
    for i, p in enumerate(paras):
        first6 = " ".join(p.split()[:6]).replace("|", "/")
        rows.append(f"| {i + 1} | {first6} | {pw[i]} | {len(ps[i])} | {','.join(map(str, beat_of.get(i + 1, ['-'])))} |")
    index = "\n".join(rows)

    # BASELINE
    all_s = [(i + 1, s) for i, ss in enumerate(ps) for s in ss]
    sl = sorted((len(words(s)), i, s) for i, s in all_s)
    one = sum(1 for s in ps if len(s) == 1)
    two3 = sum(1 for s in ps if 2 <= len(s) <= 3)
    four = sum(1 for s in ps if len(s) >= 4)
    text = "\n".join(paras)
    syl = sum(syllables(w) for w in words(text))
    fk = 0.39 * total / len(all_s) + 11.8 * syl / total - 15.59
    baseline = "\n".join([
        f"- TOTAL WORDS: {total} (tokens starting with a letter, digit or $)",
        f"- TOTAL SENTENCES: {len(all_s)} (split on . ! ? and …; P.S./AM/PM/decimals protected)",
        f"- TOTAL PARAGRAPHS: {n} (each non-empty line of the source)",
        f"- AVERAGE WORDS PER SENTENCE: {total / len(all_s):.1f}",
        f"- LONGEST SENTENCE: {sl[-1][0]} words [¶{sl[-1][1]}] \"{sl[-1][2]}\"",
        f"- SHORTEST SENTENCE: {sl[0][0]} word(s) [¶{sl[0][1]}] \"{sl[0][2]}\"",
        f"- AVERAGE WORDS PER PARAGRAPH: {total / n:.1f}",
        f"- PARAGRAPH LENGTH SPREAD (by sentence count): 1 sentence = {one} ({one / n:.0%}); 2-3 = {two3} ({two3 / n:.0%}); 4+ = {four} ({four / n:.0%})",
        f"- READING GRADE LEVEL: Flesch-Kincaid grade {fk:.1f} (method: 0.39×words/sentence + 11.8×syllables/word − 15.59; syllables estimated by vowel groups)",
        f"- ESTIMATED READ TIME: {total / 200:.1f} minutes (words ÷ 200)",
    ])

    # LINE-LEVEL COUNTS
    lw = [w.lower().strip(".,'’") for w in words(text)]
    you_set = {"you", "your", "you're", "you’re", "yourself", "you've", "you’ve", "you'd", "you’d", "you'll", "you’ll"}
    you = sum(1 for w in lw if w in you_set)
    nt = re.findall(r"\b\w+n['’]t\b", text, re.I)
    full_neg = re.findall(r"\b(do not|did not|does not|is not|was not|cannot|can not|will not|would not|could not|have not|had not|are not)\b", text, re.I)
    caps = [c for c in re.findall(r"\b[A-Z]{2,}\b", text) if c not in ("AM", "PM", "LED", "ED", "FU", "MK", "NHS", "AHI", "CPAP", "GP", "AAP", "CTA", "CoQ")]
    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text)
    excl = [(i + 1) for i, p in enumerate(paras) if "!" in p]
    qs = [(i + 1, s) for i, ss in enumerate(ps) for s in ss if "?" in s]
    one_line = [i + 1 for i, s in enumerate(ps) if len(s) == 1]
    punct = [
        ("Full stops (excl. ellipses)", text.count(".") - 3 * text.count("...")),
        ("Commas", text.count(",")),
        ("Exclamation marks", text.count("!")),
        ("Question marks", text.count("?")),
        ("Ellipses (... or …)", text.count("...") + text.count("…")),
        ("Em dashes —", text.count("—")),
        ("Spaced hyphens used as dashes ( - )", text.count(" - ")),
        ("Colons", text.count(":")),
        ("Semicolons", text.count(";")),
        ("Double quote marks (\" “ ”)", text.count('"') + text.count("“") + text.count("”")),
        ("Parentheses (opening)", text.count("(")),
    ]
    nums = [(i + 1, mm.group(0).strip()) for i, p in enumerate(paras) for mm in re.finditer(r"[£$]?\d[\d,.:]*(\s?(%|AM|PM|am|pm|FU))?", p)]
    line = "\n".join(
        [f"- DIRECT ADDRESS: {you} uses of you/your/you're etc. = {you / total * 100:.2f} per 100 words",
         f"- CONTRACTIONS: {len(nt)} n't-forms vs {len(full_neg)} uncontracted negatives {full_neg if full_neg else ''}",
         f"- ALL-CAPS WORDS (excluding acronyms): {len(caps)} {caps}",
         f"- EMOJI: {len(emoji)} {''.join(emoji)}",
         f"- PARAGRAPHS CONTAINING '!': {excl if excl else 'none'}",
         f"- ONE-SENTENCE PARAGRAPHS: {len(one_line)} of {n} ({len(one_line) / n:.0%})",
         "- PUNCTUATION INVENTORY:"]
        + [f"  - {k}: {v}" for k, v in punct]
        + [f"- QUESTIONS: {len(qs)} sentences containing '?'"]
        + [f"  - [¶{i}] \"{s}\"" for i, s in qs]
        + [f"- DIGIT NUMBERS/PRICES/TIMES: {len(nums)}: " + "; ".join(f"[¶{i}] {v}" for i, v in nums)]
    )

    # RHYTHM
    cum = 0
    buckets = [[] for _ in range(10)]
    bpar = [set() for _ in range(10)]
    for i, ss in enumerate(ps):
        for s in ss:
            k = min(9, int(cum / total * 10))
            buckets[k].append(len(words(s)))
            bpar[k].add(i + 1)
            cum += len(words(s))
    rr = ["| Tenth | ¶ span | Sentences | Avg words/sentence | Beats in this tenth |", "|---|---|---|---|---|"]
    for k in range(10):
        b = buckets[k]
        span = sorted(bpar[k])
        bts = sorted({bb for p in span for bb in beat_of.get(p, [])})
        rr.append(f"| {k * 10}-{k * 10 + 10}% | ¶{span[0]}-{span[-1]} | {len(b)} | {sum(b) / len(b):.1f} | {', '.join(map(str, bts))} |")
    rhythm = "\n".join(rr)

    # BEAT WORDS
    covered = [k for a, z, _ in beats for k in range(a, z + 1)]
    missing = sorted(set(range(1, n + 1)) - set(covered))
    dup = sorted(k for k, c in Counter(covered).items() if c > 1)
    bw = ["| Beat | Label | ¶ range | Words | % of total | Starts at |", "|---|---|---|---|---|---|"]
    formula = []
    for b, (a, z, label) in enumerate(beats, 1):
        w = sum(pw[a - 1:z])
        bw.append(f"| {b} | {label} | ¶{a}-{z} | {w} | {w / total:.1%} | {pos(pw, a - 1, total)} |")
        formula.append(f"{label.upper()} ({w}w, {w / total:.0%})")
    bsum = sum(sum(pw[a - 1:z]) for a, z, _ in beats)
    bw.append(f"\nCheck: beat words sum to {bsum} of {total}. Unassigned ¶: {missing or 'none'}. Double-counted ¶: {dup or 'none'}.")
    bw.append("\n**Formula line:** " + " → ".join(formula))
    beatwords = "\n".join(bw)

    for k, v in {"{{INDEX}}": index, "{{BASELINE}}": baseline, "{{LINE}}": line, "{{RHYTHM}}": rhythm, "{{BEATWORDS}}": beatwords}.items():
        t = t.replace(k, v)
    open(out, "w", encoding="utf-8").write(t)
    print(f"wrote {out}: {n} paragraphs, {total} words, unassigned={missing}, dup={dup}")


if __name__ == "__main__":
    main()
