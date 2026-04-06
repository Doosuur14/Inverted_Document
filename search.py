import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Load the inverted index
index = {}
with open("inverted_index.txt", "r", encoding="utf-8") as f:
    for line in f:
        lemma, docs = line.strip().split(": ")
        index[lemma] = set(docs.split())

all_docs = set()
for docs in index.values():
    all_docs.update(docs)

def evaluate(query):
    tokens = query.lower().replace("(", " ( ").replace(")", " ) ").split()

    def parse(tokens):
        stack = []

        while tokens:
            token = tokens.pop(0)

            if token == "(":
                stack.append(parse(tokens))

            elif token == ")":
                break

            elif token == "and":
                right = parse(tokens)
                left = stack.pop()
                stack.append(left & right)

            elif token == "or":
                right = parse(tokens)
                left = stack.pop()
                stack.append(left | right)

            elif token == "not":
                right = parse(tokens)
                stack.append(all_docs - right)

            else:
                lemma = lemmatizer.lemmatize(token)  # lemmatize query token
                stack.append(index.get(lemma, set()))

        return stack[0]

    return parse(tokens)

# Example usage
query = input("Enter query: ")
result = evaluate(query)
print("Matching documents:", result)