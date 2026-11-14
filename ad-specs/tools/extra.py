"""Extra counts: python3 extra.py <source> <mode> [args]
modes: terms t1,t2,...   -> count + ¶refs of each term (case-insensitive, word-boundary)
       gap a-b,c-d,...   -> words from start of ¶a to start of ¶b
       pos a,b,...       -> % position of ¶ starts
       short N           -> sentences with <= N words (fragment proxy)
"""
import re, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from measure import paragraphs, sentences, words
src, mode = sys.argv[1], sys.argv[2]
paras = paragraphs(src); pw = [len(words(p)) for p in paras]; total = sum(pw)
if mode == "terms":
    for t in sys.argv[3].split(","):
        refs = [i + 1 for i, p in enumerate(paras) for _ in re.finditer(r"\b" + re.escape(t) + r"\b", p, re.I)]
        print(f"{t}: {len(refs)} {sorted(set(refs))}")
elif mode == "gap":
    for g in sys.argv[3].split(","):
        a, b = (int(x) for x in g.split("-"))
        print(f"¶{a}->¶{b}: {sum(pw[a-1:b-1])} words")
elif mode == "pos":
    for a in sys.argv[3].split(","):
        a = int(a); print(f"¶{a}: {sum(pw[:a-1])/total:.0%}")
elif mode == "short":
    n = int(sys.argv[3]); ss = [(i+1, s) for i, p in enumerate(paras) for s in sentences(p) if len(words(s)) <= n]
    print(f"sentences <= {n} words: {len(ss)}"); print("; ".join(f"[¶{i}] {s}" for i, s in ss[:400]))
