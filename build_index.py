import os
import re
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import nltk
import ssl

# Fix SSL issue for NLTK on macOS
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Ensure NLTK data is available
nltk.download('wordnet')
nltk.download('omw-1.4')

folder = "text-files"
index = {}
lemmatizer = WordNetLemmatizer()

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(folder, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = tokenize(text)

    for word in words:
        lemma = lemmatizer.lemmatize(word)
        if lemma not in index:
            index[lemma] = set()
        index[lemma].add(filename)

# Save the inverted index
with open("inverted_index.txt", "w", encoding="utf-8") as f:
    for lemma in sorted(index.keys()):
        docs = " ".join(sorted(index[lemma]))
        f.write(f"{lemma}: {docs}\n")

print("✅ Lemmatized inverted index created!")