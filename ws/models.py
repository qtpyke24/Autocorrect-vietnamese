import os
from collections import defaultdict

def load_dict():
    data_path = "Viet74K.txt"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} not found.")
    with open(data_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end = False
        self.word = None
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children[char]
        node.is_end = True
        node.word = word

    def search_prefix(self, prefix, max_results=3):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_words(node,prefix,max_results)
    def _collect_words(self, node, prefix, max_results, words=None):
        if words is None:
            words = []
        if len(words) >= max_results:
            return words
        if node.is_end and node.word:
            words.append(node.word)
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, max_results, words)
        return words
dictionary = load_dict()
trie = Trie()
for word in dictionary:
    trie.insert(word)