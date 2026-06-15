# print out CWE distribution from commits_cwe_map.json
from pathlib import Path
import json
from collections import Counter

dataset_path = Path(__file__).resolve().with_name("commits_cwe_map.json")

with dataset_path.open("r") as f:
    commits_cwe_map = json.load(f)

cwe_counter = Counter(commits_cwe_map.values())

print("CWE Distribution in Dataset:")
print("-" * 40)
for cwe, count in sorted(cwe_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"{cwe}: {count} samples")
print("-" * 40)
print(f"Total unique CWEs: {len(cwe_counter)}")
print(f"Total samples: {sum(cwe_counter.values())}")
