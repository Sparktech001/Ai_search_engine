import pandas as pd
data = pd.read_csv("raw_code.csv")

function_calls = data["Function Calls"].dropna().astype(str)

words = []
for funcs in function_calls:
    for f in funcs.split(","):
        f = f.strip()
        if f:
            words.append(f)

class Node:
    def __init__(self):
        self.children = {}
        self.end_word = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.end_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end_word

    def autocomplete(self, prefix):
        words = []
        node = self.root
        for char in prefix:
            if char not in node.children:
                return words
            node = node.children[char]

        def dfs(current_node, path):
            if current_node.end_word:
                words.append("".join(path))
            for c, child in current_node.children.items():
                dfs(child, path + [c])

        dfs(node, list(prefix))
        return words
trie = Trie()
for word in words:
    trie.insert(word)

users_serch = input("Enter a funciton to return True or False: ")
users_autocomplete = input("Enter a function to autocomplete: ")


print(f"This is your search result: {trie.search(users_serch)}")
print(f"These are the suggestions form your search: {trie.autocomplete(users_autocomplete)}")

