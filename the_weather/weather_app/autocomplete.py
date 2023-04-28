class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._suggestions_helper(node, prefix)

    def _suggestions_helper(self, node, prefix):
        suggestions = []
        if node.is_end_of_word:
            suggestions.append(prefix)
        for char, child_node in node.children.items():
            suggestions += self._suggestions_helper(child_node, prefix + char)
        return suggestions

# Initialize the Trie with a list of cities
trie = Trie()
cities = ['London', 'New York', 'Tokyo', 'Los Angeles', 'Paris', 'Berlin']
for city in cities:
    trie.insert(city.lower())
def get_city_suggestions(prefix):
    return trie.suggestions(prefix.lower())
