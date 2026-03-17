import os
import re
from bs4 import BeautifulSoup

folder = "text-files"
index = {}

def tokenize(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words

for filename in os.listdir(folder):
    if not filename.endswith((".html", ".txt")):
        continue

    filepath = os.path.join(folder, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    words = tokenize(text)

    for word in words:
        if word not in index:
            index[word] = set()
        index[word].add(filename)


with open("inverted_index.txt", "w", encoding="utf-8") as f:
    for word in sorted(index.keys()):
        docs = " ".join(sorted(index[word]))
        f.write(f"{word}: {docs}\n")

print("Inverted index created!")