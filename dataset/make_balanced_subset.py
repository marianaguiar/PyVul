import json
import random
import collections

SRC = "pyvul_64cwes_all.json"
DST = "pyvul_64cwes_balanced200.json"
CAP = 6
SEED = 42

random.seed(SEED)

data = json.load(open(SRC))
by_cwe = collections.defaultdict(list)
for d in data:
    by_cwe[d["true_cwe"]].append(d)

subset = []
for cwe, items in by_cwe.items():
    random.shuffle(items)
    subset.extend(items[:CAP])

random.shuffle(subset)

json.dump(subset, open(DST, "w"), indent=2)

print(f"{len(subset)} samples across {len(by_cwe)} CWEs")
counts = collections.Counter(d["true_cwe"] for d in subset)
for cwe, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(cwe, n)
