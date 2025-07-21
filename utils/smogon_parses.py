import requests
import re
import pandas as pd

# URL of the usage stats file
url = "https://www.smogon.com/stats/2025-06/gen9ou-1500.txt"

# Download the file
response = requests.get(url)
text = response.text

# Extract the usage table section
lines = text.splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith("+ ---- +"))
data_lines = lines[start + 2:]  # Skip header and separator

# Parse each line
pattern = r"\| *(\d+) *\| ([\w\-\. ']+) *\| ([\d\.]+)% *\| (\d+) *\| ([\d\.]+)% *\| ([\d\.]+)% *\| ([\d\.]+)% *\|"
parsed_data = []

for line in data_lines:
    match = re.match(pattern, line)
    if match:
        rank, name, usage, raw, raw_pct, real_pct, avg_pct = match.groups()
        parsed_data.append({
            "Rank": int(rank),
            "Pokémon": name.strip(),
            "Usage %": float(usage),
            "Raw": int(raw),
            "Raw %": float(raw_pct),
            "Real %": float(real_pct),
            "Avg %": float(avg_pct)
        })

# Convert to DataFrame
df = pd.DataFrame(parsed_data)
print(df.head())
