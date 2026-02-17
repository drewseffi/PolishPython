import string
from collections import Counter

names = {"Scrooge"}

def main():
    books = read_books("Books.txt")
    books = remove_person_names(books)
    books = decapitalize(books)
    books = remove_grammer(books)
    count_words(books)

def remove_person_names(books):
    words = books.split()
    return " ".join(word for word in words if word not in names)

def decapitalize(books):
    books = books.lower()
    return books

def remove_grammer(books):
    translator = str.maketrans('', '', string.punctuation + "—")
    clean_text = books.translate(translator)
    clean_text = " ".join(clean_text.split())
    return clean_text

def read_books(filename):
    with open(filename) as f:
        return f.read()
    
def count_words(books):
    words = Counter(books.split())
    print(words.most_common(50))
    

main()