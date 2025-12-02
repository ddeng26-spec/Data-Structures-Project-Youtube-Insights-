import matplotlib.pyplot as plt
import math
import pandas as pd


def clean_youtube_search_history(input_file, output_file):
    
    # Read the raw CSV file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = []
        lines = file.readlines() 
    #with - context manager to ensure file is properly opened and closed
    #open - function to open the file (input_file) in read mode ('r') with UTF-8 encoding (Standard text for Computers)
    #readlines - method to read all lines and store them in a list 
    
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
            search_term = line[12:].strip()
            
            # Get the timestamp from the next line
            if i + 1 < len(lines):
                timestamp_line = lines[i + 1].strip().strip('"')
                
                # Clean up special characters
                timestamp_clean = timestamp_line.replace('â€¯', ' ').replace(' PST', '').strip()
                

                # Parse datetime
                dt = pd.to_datetime(timestamp_clean) # Using pandas to create datetime object which stores date and time info
                
                # Store the data
                search_terms.append(search_term)
                dates.append(dt.date()) # Using dt.date() to extract only the date part 
                times.append(dt.time()) # Using dt.time() to extract only the time part 
        i += 1
    
    # Create DataFrame
    cleaned_df = pd.DataFrame({
        'search_term': search_terms,
        'date': dates,
        'time': times
    })
    
    cleaned_df.to_csv(output_file, index=False)
    return cleaned_df


input_file = 'search-history.csv'
output_file = 'cleaned_youtube_search_history.csv'
df = clean_youtube_search_history(input_file, output_file)


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

    

    def findMin(self):
        words = []
        minVal = 100000
        for word in self.history:
            if self.history[word] == minVal:
                words.append(word)
            elif self.history[word] < minVal:
                words = [word]
                minVal = self.history[word]
        
        return words, minVal
    
    def findMax(self):
        words = []
        maxVal = 0
        for word in self.history:
            if self.history[word] == maxVal:
                words.append(word)
            elif self.history[word] > maxVal:
                words = [word]
                maxVal = self.history[word]
        
        return words, maxVal
        

    def findAverage(self):
        sum = 0
        count = len(self.history)
        for word in self.history:
            sum += self.history[word]
        return sum / count
    
    def findStdDev(self):
        avg = self.findAverage()
        count = len(self.history)
        sum = 0
        for word in self.history:
            sum += ((self.history[word] - avg)**2)
        placeholder = sum / (count - 1)
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
        print()




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

# Process each search individually
for search_term in df['search_term']:
    yt.search(search_term)

yt.summary()
    


