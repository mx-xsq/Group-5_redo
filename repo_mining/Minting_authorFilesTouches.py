import csv
import json
import os
import requests

# === Customize these ===
repo = 'scottyab/rootbeer'
lstTokens = ["123"]  # tokens
SOURCE_EXTENSIONS = ('.java', '.kt', '.py', '.cpp', '.c', '.h', '.js', '.ts')

# ======
file = repo.split('/')[1]
input_csv_path = f'data/file_{file}.csv'
output_csv_path = f'data/authors_{file}.csv'

# === GitHub authentication ===
def github_auth(url, lsttoken, ct):
    jsonData = None
    ct = ct % len(lsttoken)
    headers = {'Authorization': f'Bearer {lsttoken[ct]}'}
    try:
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(f"Error during GitHub API call: {e}")
    return jsonData, ct

# === Step 1: Read filtered list of source files ===
def read_source_files(path, extensions):
    source_files = set()
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) == 0:
                continue
            filename = row[0].strip()
            if filename.endswith(extensions):
                source_files.add(filename)
    return source_files

# === Step 2: Gather authors and dates per source file ===
def gather_authors_dates(source_files, lstTokens, repo):
    ipage = 1
    ct = 0
    file_author_data = {f: [] for f in source_files}

    while True:
        url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
        commits, ct = github_auth(url, lstTokens, ct)
        if not commits:
            break
        for commit in commits:
            sha = commit['sha']
            sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
            commit_data, ct = github_auth(sha_url, lstTokens, ct)

            try:
                author = commit_data['commit']['author']['name']
                date = commit_data['commit']['author']['date']
                files = commit_data.get('files', [])
            except (KeyError, TypeError):
                continue

            for f in files:
                filename = f.get('filename')
                if filename in file_author_data:
                    file_author_data[filename].append((author, date))
        ipage += 1
    return file_author_data

# === Step 3: Write to CSV ===
def write_output(path, file_author_data):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Author", "Date"])
        for filename, touches in file_author_data.items():
            for author, date in touches:
                writer.writerow([filename, author, date])

# === Execute ===
source_files = read_source_files(input_csv_path, SOURCE_EXTENSIONS)
print(f"Found {len(source_files)} source files.")
file_author_data = gather_authors_dates(source_files, lstTokens, repo)
write_output(output_csv_path, file_author_data)
print(f"Saved authors and dates to {output_csv_path}")
