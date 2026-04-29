import json, re

f = open(r"e:\Downloads\--ANTIGRAVITY store\IDE-NEXUS\PROJECT\WIKI-FARM\NEXUS-FARM-DNA\dna_state.json", "r", encoding="utf-8")
data = json.load(f)
f.close()

text = "\n".join(data["fragments"])
names = sorted(set(re.findall(r'\*\*([A-Z][A-Z0-9_.:-]+(?:-[A-Z0-9_.]+)*)\*\*', text)))
for n in names:
    print(n)
print(f"\nTotal: {len(names)}")
