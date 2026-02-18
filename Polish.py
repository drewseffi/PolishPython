import string
import questionary
import nltk
import re
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    print("nltk datasets not detected, installing...")
else:
    print("nltk datasets detected, running PolishPython...")
from nltk import tokenize
from collections import Counter

# Premade list of names that occur in the texts
names = {"scrooge", "scroogea", "krystian", "krystiana", "piotr"}

def main():
    # Opens the file before running anything else
    books = read_books("Books.txt")

    # Fun ascii art from https://patorjk.com/software/taag/
    print(r"""*---------------------------------------------------------------------------------------------------------*""")
    print(r""" /$$$$$$$           /$$ /$$           /$$       /$$$$$$$              /$$     /$$                          """)
    print(r"""| $$__  $$         | $$|__/          | $$      | $$__  $$            | $$    | $$                          """)
    print(r"""| $$  \ $$ /$$$$$$ | $$ /$$  /$$$$$$$| $$$$$$$ | $$  \ $$ /$$   /$$ /$$$$$$  | $$$$$$$   /$$$$$$  /$$$$$$$ """)
    print(r"""| $$$$$$$//$$__  $$| $$| $$ /$$_____/| $$__  $$| $$$$$$$/| $$  | $$|_  $$_/  | $$__  $$ /$$__  $$| $$__  $$""")
    print(r"""| $$____/| $$  \ $$| $$| $$|  $$$$$$ | $$  \ $$| $$____/ | $$  | $$  | $$    | $$  \ $$| $$  \ $$| $$  \ $$""")
    print(r"""| $$     | $$  | $$| $$| $$ \____  $$| $$  | $$| $$      | $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$  | $$""")
    print(r"""| $$     |  $$$$$$/| $$| $$ /$$$$$$$/| $$  | $$| $$      |  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$/| $$  | $$""")
    print(r"""|__/      \______/ |__/|__/|_______/ |__/  |__/|__/       \____  $$   \___/  |__/  |__/ \______/ |__/  |__/""")
    print(r"""                                                          /$$  | $$                                        """)
    print(r"""                                                         |  $$$$$$/                                        """)
    print(r"""                                                          \______/                                         """)
    print(r"""*---------------------------------------------------------------------------------------------------------*""")
    print("")

    # Text for choice selection, easier and cleaner to predefine here
    choice_text = ["Show most common words", 
                   "Search for a word (shows word in sentences)"]

    # Uses questionary to add a multiple choice selection menu
    choice = questionary.select("What would you like to do?", choices=[choice_text[0], choice_text[1]]).ask()

    # If user wants to see the most common words
    if choice == choice_text[0]:
        # Sanitizes the text
        books = decapitalize(books)
        books = remove_person_names(books)
        books = remove_grammar(books)

        # Asks user for input on how many words to show and displays them
        print("How many words would you like to show?")
        num_of_words = input()
        count_words(books, num_of_words)

    # If user wants to look up a sentence containing a word
    elif choice == choice_text[1]:
        print("Please enter a word you would like to see in a sentence (include accents)")
        search = input()
        get_sentences(books, search)

def get_sentences(books, s):
    print("")
    sentences = tokenize.sent_tokenize(books)
    pattern = re.compile(rf'\b{re.escape(s)}\b', re.IGNORECASE)

    matches = [sentence for sentence in sentences if pattern.search(sentence)]

    counter = 1

    for sentence in matches:
        print(f"{counter}) {sentence}")
        print("")
        counter += 1


# Removes names by checking each word againts a premade list of names
def remove_person_names(books):
    words = books.split()
    return " ".join(word for word in words if word not in names)

# Turns all text lower case to provide a more accurate count
def decapitalize(books):
    books = books.lower()
    return books

# Removes all grammar for use when counting words
def remove_grammar(books):
    translator = str.maketrans('', '', string.punctuation + "—")
    clean_text = books.translate(translator)
    clean_text = " ".join(clean_text.split())
    return clean_text

# Opens the txt file (needs declared as utf-8 on windows)
def read_books(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()
    
# Counts all occurances of words in the file and prints them to console
def count_words(books, n):
    # Using the Python Counter package
    words = Counter(books.split())
    top_words = words.most_common(int(n))

    # Loops through the dict and formats them nicely with :> 
    for rank, (word, count) in enumerate(top_words, start=1):
        print(f"{rank:>4}. {word:<15} {count:>6}")

    

main()