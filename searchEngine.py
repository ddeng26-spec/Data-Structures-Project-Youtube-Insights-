import matplotlib.pyplot as plt
import math
import pandas as pd


def clean_youtube_search_history(input_file, output_file):

    # Read the raw CSV file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        #with - context manager to ensure file is properly opened and closed
        #open - function to open the file (input_file) in read mode ('r') with UTF-8 encoding (Standard text for Computers)
        #readlines - method to read all lines and store them in a list
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Make sure the file exists.")
        return pd.DataFrame()

    # Lists to store cleaned data
    search_terms = []
    dates = []
    times = []

    # Process the file line by line
    i = 0
    while i < len(lines):
        line = lines[i].strip().strip('"')

        # Look for search entries
        if line.startswith("Searched for"):
            # Remove "Searched for" prefix
            search_term = line[14:].strip()

            # Get the timestamp from the next line
            if i + 1 < len(lines):
                timestamp_line = lines[i + 1].strip().strip('"')

                # Clean up special characters
                timestamp_clean = timestamp_line.replace('â€¯', ' ').replace(' PST', '').strip()

                # Parse datetime
                try:
                    dt = pd.to_datetime(timestamp_clean) # Using pandas to create datetime object which stores date and time info

                    # Store the data
                    search_terms.append(search_term)
                    dates.append(dt.date()) # Using dt.date() to extract only the date part
                    times.append(dt.time()) # Using dt.time() to extract only the time part
                except:
                    # Keep term even if date fails
                    search_terms.append(search_term)
                    dates.append(None)
                    times.append(None)
            else:
                 search_terms.append(search_term)
                 dates.append(None)
                 times.append(None)
        i += 1

    # Create DataFrame
    cleaned_df = pd.DataFrame({
        'search_term': search_terms,
        'date': dates,
        'time': times
    })

    cleaned_df.to_csv(output_file, index=False)
    return cleaned_df


class YTSearch: # Overarching class. All methods / data structures for project can be accessed through this.
    def __init__(self):
        self.history = {}
        self.bst = None
        # We use a 'set' because checking "if word in set" is faster than a list - hashing the word is O(1) instead of O(N)
        self.STOP_WORDS = {
            "a", "the", "and", "or", "but", "is", "are", "was", "were",
            "of", "in", "on", "at", "to", "for", "with", "by", "from",
            "vs", "how", "what", "why", "who", "i", "my", "me", "it",
            "this"
        }


    def search(self, text): # creates a search. Splits up search string into only words then updates the self.history table with new frequencies
        if not isinstance(text, str):
            return

        text = text.lower()
        for punctuation in ',.?;":!-':
            text = text.replace(punctuation, "")
        words = text.split()
        for word in words:
            if word in self.STOP_WORDS: #if the word is mentioned in the set, then we skip
                continue
            if word in self.history:
                self.history[word] += 1
            else:
                self.history[word] = 1

    def createBST(self): # Creates a BST using the current history hash table. Word frequency is used to sort the tree
        tree = BST()
        for word in self.history:
            tree.insert(word, self.history[word])
        self.bst = tree


    def findMin(self):
        if not self.history: return [], 0

        minVal = min(self.history.values())
        words = [word for word, count in self.history.items() if count == minVal]

        return words, minVal

    def findMax(self):
        if not self.history: return [], 0

        maxVal = max(self.history.values())
        words = [word for word, count in self.history.items() if count == maxVal]

        return words, maxVal


    def findAverage(self):
        if len(self.history) == 0: return 0
        sum_val = sum(self.history.values())
        count = len(self.history)
        return sum_val / count

    def findStdDev(self):
        count = len(self.history)
        if count < 2: return 0
        avg = self.findAverage()
        sum_val = 0
        for word in self.history:
            sum_val += ((self.history[word] - avg)**2)
        placeholder = sum_val / (count - 1)
        return math.sqrt(placeholder)

    def frequency_by_word_length(self):
        three_or_fewer = 0
        four_or_five = 0
        six_or_seven = 0
        eight_plus = 0
        for word in self.history:
            length = len(word)
            if length <= 3:
                three_or_fewer += 1
            elif length == 4 or length == 5:
                four_or_five += 1
            elif length == 6 or length == 7:
                six_or_seven += 1
            else:
                eight_plus += 1
        categories = ['3 Letters or Less','4 or 5 Letters', '6 or 7 Letters', '8 or more Letters']
        frequencies = [three_or_fewer, four_or_five, six_or_seven, eight_plus]
        plt.bar(categories, frequencies)
        plt.xlabel('Number of Letters in Words')
        plt.ylabel('Frequency')
        plt.title('Frequency Distribution of Word Lengths')
        plt.show()

    def findWord(self, word):
        for key in self.history:
            if key == word:
                print("word Found")
                return self.history[word]
        print("Word Not Found")
        return None

    def summary(self):
        self.createBST()

        num_words = len(self.history)
        min_freq_words, min_freq = self.findMin()
        max_freq_words, max_freq = self.findMax()
        avg_freq = round(self.findAverage(), 3)
        std_dev = round(self.findStdDev(), 3)
        print()
        print("Summary of Search History:")
        print(f"Total Number of Unique Words Searched: {num_words}")
        print(f"The following words {min_freq_words} appeared the least with frequency: {min_freq}")
        print(f"The following words {max_freq_words} appeared the most with frequency: {max_freq}")
        print(f"The Average Frequency of Words Searched: {avg_freq}")
        print(f"The Standard Deviation from the Average: {std_dev}")

        print("\n--- Top 10 Trending Keywords ---")
        top_trends = self.bst.get_top_k(10)
        for rank, (word, count) in enumerate(top_trends, 1):
            print(f"#{rank}: {word} ({count} searches)")
        print()




class Node:
    def __init__(self, word, value): # Standard tree node for a word. Contains both word itself and its frequency
        self.word = word
        self.value = value
        self.left = None
        self.right = None

    def inorder(self, currentNode):
        if currentNode:
            self.inorder(currentNode.left)
            print(f"{currentNode.word}:{currentNode.value}")
            self.inorder(currentNode.right)

    def reverse_inorder(self, node, counter, limit, results):
        if node is None or counter[0] >= limit:
            return
        self.reverse_inorder(node.right, counter, limit, results)
        if counter[0] < limit:
            results.append((node.word, node.value))
            counter[0] += 1
        self.reverse_inorder(node.left, counter, limit, results)


class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, value):
        new_node = Node(word, value)
        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if current.word == word:
                return
            elif value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def inorder(self):
        if self.root:
            self.root.inorder(self.root)

    def get_top_k(self, k):
        results = []
        counter = [0]
        if self.root:
            self.root.reverse_inorder(self.root, counter, k, results)
        return results


input_file = 'search-history.csv'
output_file = 'cleaned_youtube_search_history.csv'
df = clean_youtube_search_history(input_file, output_file)

if not df.empty:
    yt = YTSearch() # Sample usage

    # Process each search individually
    for search_term in df['search_term']:
        yt.search(search_term)

    yt.summary()
