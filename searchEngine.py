class YTSearch: # Overarching class. All methods / data structures for project can be accessed through this.
    def __init__(self):
        self.history = {}
        self.bst = None


    def search(self, text): # creates a search. Splits up search string into only words then updates the self.history table with new frequencies
        text = text.lower()
        for punctuation in ',.?;":!-':
            text = text.replace(punctuation, "")
        words = text.split()
        for word in words:
            if word in self.history:
                self.history[word] += 1
            else:
                self.history[word] = 1

    def createBST(self): # Creates a BST using the current history hash table. Word frequency is used to sort the tree
        tree = BST()
        for word in self.history:
            tree.insert(word, self.history[word])
        self.bst = tree


class Node:
    def __init__(self, word, value): # Standard tree node for a word. Contains both word itself and its frequency
        self.word = word
        self.value = value
        self.left = None
        self.right = None

    def insert(self, word, value):
        if self.word == word:
            raise Exception("Word already in tree")
        elif self.value > value:
            if self.left:
                self.left.insert(word, value)
            else:
                self.left = Node(word, value)
        else:
            if self.right:
                self.right.insert(word, value)
            else:
                self.right = Node(word, value)

    def inorder(self, currentNode):
        if currentNode:
            self.inorder(currentNode.left)
            print(f"{currentNode.word}:{currentNode.value}")
            self.inorder(currentNode.right)

class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, value):
        if self.root:
            self.root.insert(word, value)
        else:
            self.root = Node(word, value)

    def inorder(self):
        if self.root:
            self.root.inorder(self.root)


yt = YTSearch() # Sample usage

yt.search("Minecraft Tutorial!!!")
yt.search("How to tie a tie?")
yt.search("How to trickshot??!:")

print(yt.history)

yt.createBST()

yt.bst.inorder()
    


