import re


index = {}

with open("inverted_index.txt", "r", encoding="utf-8") as f:
    for line in f:
        word, docs = line.strip().split(": ")
        index[word] = set(docs.split())


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
                stack.append(index.get(token, set()))

        return stack[0]

    return parse(tokens)


query = input("Enter query: ")

result = evaluate(query)

print("Matching documents:", result)