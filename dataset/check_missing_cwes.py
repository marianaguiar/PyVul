#!/usr/bin/env python3
"""Check which CWEs in PyVul are not present in software_development_cwes.json"""

from pathlib import Path
import json
from collections import Counter

# Load PyVul CWEs
pyvul_path = Path(__file__).resolve().with_name("commits_cwe_map.json")
with pyvul_path.open("r") as f:
    commits_cwe_map = json.load(f)

# Get unique CWEs from PyVul (format: CWE-XXX)
pyvul_cwes = set(commits_cwe_map.values())

# Load software development CWEs
sw_dev_path = Path(__file__).resolve().parent.parent.parent / "processed" / "software_development_cwes.json"
with sw_dev_path.open("r") as f:
    sw_dev_cwes_data = json.load(f)

# Create set of CWE-IDs from software development CWEs (format: XXX)
sw_dev_cwe_ids = {cwe["CWE-ID"] for cwe in sw_dev_cwes_data}

# Also create set with CWE- prefix for comparison
sw_dev_cwes_formatted = {f"CWE-{cwe_id}" for cwe_id in sw_dev_cwe_ids}

# Find CWEs in PyVul that are NOT in software development CWEs
missing_cwes = pyvul_cwes - sw_dev_cwes_formatted

# Get counts for missing CWEs
cwe_counter = Counter(commits_cwe_map.values())
missing_cwes_with_counts = [(cwe, cwe_counter[cwe]) for cwe in sorted(missing_cwes)]

print("=" * 60)
print("CWEs in PyVul NOT present in software_development_cwes.json")
print("=" * 60)
print()

if missing_cwes:
    print(f"Found {len(missing_cwes)} CWEs in PyVul that are missing:")
    print("-" * 60)
    total_samples = 0
    for cwe, count in sorted(missing_cwes_with_counts, key=lambda x: x[1], reverse=True):
        print(f"{cwe}: {count} samples")
        total_samples += count
    print("-" * 60)
    print(f"Total samples affected: {total_samples}")
else:
    print("✓ All PyVul CWEs are present in software_development_cwes.json")

print()
print("Summary:")
print(f"  PyVul unique CWEs: {len(pyvul_cwes)}")
print(f"  Software Dev CWEs: {len(sw_dev_cwes_formatted)}")
print(f"  Missing from SW Dev: {len(missing_cwes)}")
print(f"  Coverage: {(len(pyvul_cwes) - len(missing_cwes)) / len(pyvul_cwes) * 100:.1f}%")
print()
