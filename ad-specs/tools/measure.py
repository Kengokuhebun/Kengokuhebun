"""Measure a long-form ad for the Dissect Winner protocol.

Usage: python3 measure.py <source.txt> [--index] [--beats "1-12,13-20,..."]

Every non-empty line of the source is one paragraph (¶1, ¶2, ...).
Prints baseline measurements, the paragraph index, line-level counts and,
when beat ranges are given, words and % per beat plus a rhythm map by tenths.
"""
import re
import sys
from collections import Counter

ABBREV = re.compile(r"\b(P\.(P\.)*S|AM|PM|Mr|Mrs|Dr|vs|etc)\.", re.I)


def paragraphs(path):
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def words(text):
    return re.findall(r"[A-Za-z0-9$][A-Za-z0-9'’,.$%\-]*", text)


def sentences(text):
    t = ABBREV.sub(lambda m: m.group(0).replace(".", "§"), text)
    t = re.sub(r"(\d)\.(\d)", r"\1§\2", t)
    parts = re.split(r"(?<=[.!?…])[\"”’)]*\s+|(?<=\.\.\.)\s+", t)
    return [p.replace("§", ".") for p in parts if words(p)]


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith("le"):
        n -= 1
    return max(1, n)


def main():
    path = sys.argv[1]
    paras = paragraphs(path)
    pw = [len(words(p)) for p in paras]
    ps = [sentences(p) for p in paras]
    total_w = sum(pw)
    all_s = [(i + 1, s) for i, ss in enumerate(ps) for s in ss]
    sl = [(len(words(s)), i, s) for i, s in all_s]
    text = "\n".join(paras)

    print(f"TOTAL PARAGRAPHS: {len(paras)}")
    print(f"TOTAL WORDS: {total_w}")
    print(f"TOTAL SENTENCES: {len(all_s)}")
    print(f"AVG WORDS/SENTENCE: {total_w / len(all_s):.1f}")
    print(f"AVG WORDS/PARAGRAPH: {total_w / len(paras):.1f}")
    lo = min(sl)
    hi = max(sl)
    print(f"LONGEST SENTENCE: {hi[0]}w [¶{hi[1]}] {hi[2][:140]}")
    print(f"SHORTEST SENTENCE: {lo[0]}w [¶{lo[1]}] {lo[2]}")
    one = [i + 1 for i, s in enumerate(ps) if len(s) == 1]
    two3 = [i + 1 for i, s in enumerate(ps) if 2 <= len(s) <= 3]
    four = [i + 1 for i, s in enumerate(ps) if len(s) >= 4]
    n = len(paras)
    print(f"PARAS BY SENTENCES: 1={len(one)} ({len(one)/n:.0%}) 2-3={len(two3)} ({len(two3)/n:.0%}) 4+={len(four)} ({len(four)/n:.0%})")
    print(f"  4+ sentence paras: {four}")
    syl = sum(syllables(w) for w in words(text))
    fk = 0.39 * total_w / len(all_s) + 11.8 * syl / total_w - 15.59
    print(f"FLESCH-KINCAID GRADE (regex syllable estimate): {fk:.1f}")
    print(f"READ TIME @200wpm: {total_w / 200:.1f} min")

    lw = [w.lower().strip(".,'’") for w in words(text)]
    you = sum(1 for w in lw if w in ("you", "your", "you're", "you’re", "yourself", "you've", "you’ve", "you'd", "you’d", "you'll"))
    print(f"YOU/YOUR COUNT: {you} ({you / total_w * 100:.2f} per 100 words)")
    contractions = re.findall(r"\b\w+['’](t|s|re|ve|d|ll|m)\b", text)
    print(f"CONTRACTIONS (apostrophe forms incl. possessive 's): {len(contractions)}")
    nt = re.findall(r"\b\w+n['’]t\b", text, re.I)
    full_neg = re.findall(r"\b(do not|did not|does not|is not|was not|can not|cannot|will not|would not|could not|have not|had not)\b", text, re.I)
    print(f"  n't forms: {len(nt)} | uncontracted negatives: {len(full_neg)} {full_neg}")

    punct = {
        ".": text.count(".") - text.count("..."),
        ",": text.count(","),
        "!": text.count("!"),
        "?": text.count("?"),
        "... / …": text.count("...") + text.count("…"),
        "— (em dash)": text.count("—"),
        "– (en dash)": text.count("–"),
        " - (spaced hyphen)": text.count(" - "),
        ":": text.count(":"),
        ";": text.count(";"),
        'quotes " “”': text.count('"') + text.count("“") + text.count("”"),
        "( )": text.count("("),
    }
    for k, v in punct.items():
        print(f"PUNCT {k}: {v}")
    caps = re.findall(r"\b[A-Z]{2,}\b", text)
    caps = [c for c in caps if c not in ("AM", "PM", "LED", "ED", "FU", "MK", "K2", "CTA")]
    print(f"ALL-CAPS WORDS (excl. AM/PM/LED/ED/FU/MK): {len(caps)} {caps}")
    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text)
    print(f"EMOJI: {len(emoji)} {emoji}")

    q = [(i + 1, s) for i, ss in enumerate(ps) for s in ss if s.rstrip("\"”’ ").endswith("?") or "?" in s]
    print(f"QUESTIONS: {len(q)}")
    for i, s in q:
        print(f"  [¶{i}] {s}")

    nums = []
    for i, p in enumerate(paras):
        for m in re.finditer(r"\$?\d[\d,.:]*\s?(%|AM|PM|FU|th|st|nd|rd)?", p):
            nums.append((i + 1, m.group(0).strip()))
    print(f"DIGIT NUMERALS: {len(nums)}")
    print("  " + "; ".join(f"[¶{i}] {v}" for i, v in nums))
    numwords = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|sixty-one|first|second|third|half|hundred|thousand)\b", re.I)
    nw = [(i + 1, m.group(0)) for i, p in enumerate(paras) for m in numwords.finditer(p)]
    print(f"SPELLED NUMBERS/ORDINALS: {len(nw)}")
    print("  " + "; ".join(f"[¶{i}] {v}" for i, v in nw))

    if "--index" in sys.argv:
        print("\n¶ | FIRST 6 WORDS | WORDS | SENTENCES")
        for i, p in enumerate(paras):
            print(f"{i + 1} | {' '.join(p.split()[:6])} | {pw[i]} | {len(ps[i])}")

    if "--beats" in sys.argv:
        spec = sys.argv[sys.argv.index("--beats") + 1]
        covered = []
        print("\nBEAT | ¶ RANGE | WORDS | %")
        for b, rng in enumerate(spec.split(","), 1):
            a, z = (int(x) for x in rng.split("-"))
            covered.extend(range(a, z + 1))
            bw = sum(pw[a - 1:z])
            print(f"{b} | ¶{a}-{z} | {bw} | {bw / total_w:.1%}")
        missing = sorted(set(range(1, n + 1)) - set(covered))
        dup = [k for k, c in Counter(covered).items() if c > 1]
        print(f"UNASSIGNED: {missing} | DOUBLE-COUNTED: {dup}")

    print("\nRHYTHM BY TENTHS (by cumulative words)")
    cum = 0
    buckets = [[] for _ in range(10)]
    bpar = [set() for _ in range(10)]
    for i, ss in enumerate(ps):
        for s in ss:
            k = min(9, int(cum / total_w * 10))
            buckets[k].append(len(words(s)))
            bpar[k].add(i + 1)
            cum += len(words(s))
    for k in range(10):
        b = buckets[k]
        rng = f"¶{min(bpar[k])}-{max(bpar[k])}" if bpar[k] else "-"
        print(f"{k * 10}-{k * 10 + 10}% | {rng} | sentences={len(b)} | avg={sum(b) / len(b):.1f}w")

    def first(term):
        for i, p in enumerate(paras):
            if term.lower() in p.lower():
                pos = sum(pw[:i]) / total_w
                return f"¶{i + 1} ({pos:.0%} through)"
        return "Not present"

    for term in sys.argv[2:]:
        if term.startswith("--") or re.match(r"^[\d,\-]+$", term):
            continue
        print(f"FIRST '{term}': {first(term)}")


if __name__ == "__main__":
    main()
