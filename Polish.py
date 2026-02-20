import string
import questionary
import nltk
import re
import pickle
import random
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
from rich.console import Console

# Premade list of names that occur in the texts
names = {"scrooge", "scroogea", "krystian", "krystiana", "piotr"}

console = Console(highlight=False)

class Card:
    def __init__(self, word, meaning, example):
        self.word = word
        self.meaning = meaning
        self.example = example

    def edit_card(self):
        print("Word:")
        self.word = input()
        print("Meaning")
        self.meaning = input()
        print("Example:")
        self.example = input()

def art():
    # Fun ascii art from https://patorjk.com/software/taag/
    console.print(r"""[gold1]*---------------------------------------------------------------------------------------------------------*[/]""")
    console.print(r"""[white] /$$$$$$$           /$$ /$$           /$$       /$$$$$$$              /$$     /$$                          [/]""")
    console.print(r"""[white]| $$__  $$         | $$|__/          | $$      | $$__  $$            | $$    | $$                          [/]""")
    console.print(r"""[white]| $$  \ $$ /$$$$$$ | $$ /$$  /$$$$$$$| $$$$$$$ | $$  \ $$ /$$   /$$ /$$$$$$  | $$$$$$$   /$$$$$$  /$$$$$$$ [/]""")
    console.print(r"""[white]| $$$$$$$//$$__  $$| $$| $$ /$$_____/| $$__  $$| $$$$$$$/| $$  | $$|_  $$_/  | $$__  $$ /$$__  $$| $$__  $$[/]""")
    console.print(r"""[white]| $$____/| $$  \ $$| $$| $$|  $$$$$$ | $$  \ $$| $$____/ | $$  | $$  | $$    | $$  \ $$| $$  \ $$| $$  \ $$[/]""")
    console.print(r"""[red]| $$     | $$  | $$| $$| $$ \____  $$| $$  | $$| $$      | $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$  | $$[/]""")
    console.print(r"""[red]| $$     |  $$$$$$/| $$| $$ /$$$$$$$/| $$  | $$| $$      |  $$$$$$$  |  $$$$/| $$  | $$|  $$$$$$/| $$  | $$[/]""")
    console.print(r"""[red]|__/      \______/ |__/|__/|_______/ |__/  |__/|__/       \____  $$   \___/  |__/  |__/ \______/ |__/  |__/[/]""")
    console.print(r"""[red]                                                          /$$  | $$                                        [/]""")
    console.print(r"""[red]                                                         |  $$$$$$/                                        [/]""")
    console.print(r"""[red]                                                          \______/                                         [/]""")
    console.print(r"""[gold1]*---------------------------------------------------------------------------------------------------------*[/]""")
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
        print("How many sentences would you like to see?")
        num = input()
        get_sentences(books, search, num)

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
                review_cards()
                main()

            case "List all cards":
                list_all_cards()
                main()

            case "Edit card":
                found = False
                print("Please enter word you would like to edit (include accents)")
                word_to_edit = input()
                with open('data.pkl', 'rb') as f:
                    loaded_list = pickle.load(f)
                for card in loaded_list:
                    if card.word.lower() == word_to_edit.lower():
                        card.edit_card()
                        found = True
                        break

                if not found:
                    print("No card with that word found...")

                with open('data.pkl', 'wb') as f:
                    pickle.dump(loaded_list, f)

                main()

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

# Gives you a shuffled deck of cards you have created to review
def review_cards():
    with open('data.pkl', 'rb') as f:
        loaded_list = pickle.load(f)

    shuffled_list = loaded_list
    random.shuffle(shuffled_list)

    console.print("[bold red]**Type 'e' into the input to cancel**[/]")

    for card in shuffled_list:
        console.print(f"[bold red]Word:[/] {card.word}")
        if input("Press enter to reveal the meaning and example...") == "e":
            main()
            break
        console.print(f"[bold red]Meaning:[/] {card.meaning}")
        console.print(f"[bold red]Example:[/] {card.example}")
        if input("Press enter to go to next card...") == "e":
            main()
            break

    print("You have completed every card, well done!")

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
            console.print(f"[bold red]Word:[/] {obj.word}")
            console.print(f"[bold red]Meaning:[/] {obj.meaning}")
            console.print(f"[bold red]Example:[/] {obj.example}")
            console.print("")

# Creates cards and auto saves to pkl
def create_card():
    console.print("[bold red]**Type 'e' into the word input to cancel**[/]")

    # Loops so you can input multiple cards at once
    looping = True
    while looping:
        print("Word:")
        word = input()
        
        # Hard-coded stopword, needs improved
        if word.lower() == "e":
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
def get_sentences(books, s, n):
    n = int(n)
    print("")

    sentences = tokenize.sent_tokenize(books)
    pattern = re.compile(rf'\b{re.escape(s)}\b', re.IGNORECASE)

    matches = [sentence for sentence in sentences if pattern.search(sentence)]
    random.shuffle(matches)

    if not matches:
        print("No matches found.")
        return

    if n > len(matches):
        console.print(f"[bold red]Only {len(matches)} matches, displaying all...[/]")
        n = len(matches)

    for counter, sentence in enumerate(matches[:n], start=1):
        print(f"{counter}) {sentence}")
        print("")

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
        console.print(f"[bold red]{rank:>4}.[/] {word:<15} {count:>6}")

    main()

art()
main()