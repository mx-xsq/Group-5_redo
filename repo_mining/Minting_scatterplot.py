import csv
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from collections import defaultdict

# === CONFIG ===
input_csv = 'data/authors_rootbeer.csv'  # Replace with your actual authors CSV
project_start_date = None  # Will be inferred from earliest commit date

# === Step 1: Read the data ===
data = []
with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filename = row['Filename']
        author = row['Author']
        date_str = row['Date']
        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        except:
            continue
        data.append((filename, author, date))

# === Step 2: Find project start date ===
if not data:
    raise ValueError("No data found in CSV.")

project_start_date = min(d[2] for d in data)

# === Step 3: Compute weeks since project start ===
processed = []
for filename, author, date in data:
    weeks_since_start = (date - project_start_date).days // 7
    processed.append((filename, author, weeks_since_start))

# === Step 4: Encode files and authors ===
files = list(sorted(set(d[0] for d in processed)))
file_to_y = {f: i for i, f in enumerate(files)}

authors = list(sorted(set(d[1] for d in processed)))
author_to_color = {a: cm.tab20(i % 20) for i, a in enumerate(authors)}  # Up to 20 unique colors

# === Step 5: Create the scatter plot ===
plt.figure(figsize=(12, 8))
for filename, author, week in processed:
    y = file_to_y[filename]
    color = author_to_color[author]
    plt.scatter(week, y, color=color, label=author, alpha=0.7, edgecolors='k', s=40)

# === Step 6: Label formatting ===
plt.yticks(range(len(files)), files, fontsize=7)
plt.xlabel("Weeks since project start", fontsize=12)
plt.ylabel("File", fontsize=12)
plt.title("File Touches Over Time (Colored by Author)", fontsize=14)

# === Create a legend with unique authors ===
handles = []
seen = set()
for author in authors:
    if author not in seen:
        handles.append(plt.Line2D([0], [0], marker='o', color='w', label=author,
                                  markerfacecolor=author_to_color[author], markersize=8))
        seen.add(author)

plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', title="Authors")

plt.tight_layout()
plt.grid(True, axis='x', linestyle='--', alpha=0.3)
plt.show()
