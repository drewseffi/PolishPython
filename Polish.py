import string
import questionary
import nltk
import re
import pickle
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

class Card:
    def __init__(self, word, meaning, example):
        self.word = word
        self.meaning = meaning
        self.example = example

def art():
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

def main():
    # Opens the file before running anything else
    books = read_books("Books.txt")

    # Text for choice selection, easier and cleaner to predefine here
    choice_text = ["Show most common words", 
                   "Search for a word (shows word in sentences)",
                   "Flashcard mode",
                   "Exit"]

    # Uses questionary to add a multiple choice selection menu
    choice = questionary.select("What would you like to do?", choices = choice_text).ask()

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

    # If the user selects the flashcard mode
    elif choice == choice_text[2]:

        # Choices for the sub menu for flashcard mode
        flash_choice_text = ["Create new card",
                        "Review cards (test)",
                        "List all cards",
                        "Edit card",
                        "Remove a card",
                        "Remove all cards",
                        "Main menu"]
        
        flash_choice = questionary.select("What would you like do to?", choices = flash_choice_text).ask()

        # Switch for each selection
        match flash_choice:
            case "Create new card":
                create_card()
                main()

            case "Review cards (test)":
                print()

            case "List all cards":
                list_all_cards()
                main()

            case "Edit card":
                print()

            case "Remove a card":
                print("Please enter word you would like to remove (include accents)")
                word_to_remove = input()
                remove_card(word_to_remove)
                main()

            case "Remove all cards":
                remove_card(None)
                main()

            case "Main menu":
                main()

    elif choice == choice_text[3]:
        print("Goodbye <3")

# Function for removing cards, easy to reuse for removing all cards
def remove_card(word):
        with open('data.pkl', 'rb') as f:
            loaded_list = pickle.load(f)

        for obj in loaded_list:
            if word == None:
                loaded_list = []
            elif obj.word == word:
                loaded_list.remove(obj)

        with open('data.pkl', 'wb') as f:
            pickle.dump(loaded_list, f)

# Shows all cards to the user
def list_all_cards():
        with open('data.pkl', 'rb') as f:
            loaded_list = pickle.load(f)

        for obj in loaded_list:
            print(f"Word: {obj.word}")
            print(f"Meaning: {obj.meaning}")
            print(f"Example: {obj.example}")
            print("")

# Creates cards and auto saves to pkl
def create_card():
    print("**Type 'exit' into the word input to cancel**")

    # Loops so you can input multiple cards at once
    looping = True
    while looping:
        print("Word:")
        word = input()
        
        # Hard-coded stopword, needs improved
        if word.lower() == "exit":
            looping = False
            break

        print("Meaning:")
        meaning = input()
        print ("Example:")
        example = input()

        # Load the pkl file to be read, creates a new list if the file doesnt exist
        try:
            with open('data.pkl', 'rb') as f:
                loaded_list = pickle.load(f)
        except (FileNotFoundError, EOFError):
            loaded_list = []

        new_card = Card(word, meaning, example)
        loaded_list.append(new_card)

        # Save the list automatically
        with open('data.pkl', 'wb') as f:
            pickle.dump(loaded_list, f)

        print("")

def get_exit_code(i, breakword):
    if i.lower() == breakword:
        return False
    else:
        return True

# Splits the text into sentences and then searches for all sentences containting the search word
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

    main()

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

art()
main()