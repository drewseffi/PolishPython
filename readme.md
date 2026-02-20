# PolishPython

A simple Python command line tool for use in aiding Polish language learning. This tool uses public domain books taken from [Wolne Lektury](https://wolnelektury.pl/) as source material. This project is just a pet project and is not meant to be made for mass-use however I want to be able to track my progress and share it on GitHub.

## Features

- Count words in the text to show the most common words, very helpful for language learning flashcards
- Find sentences containing a selected word, good for finding out how words work in context of the language
- Flashcards built in

## The Process

### Source Material

To start with I needed to find some source material for this project. Thankfully I was able to find [Wolne Lektury](https://wolnelektury.pl/) which hosts a lot of free, public domain books in the Polish language. I then had to manually copy and paste the full books into a text file `Books.txt`. I started with just two books but this grew over time to get better results.

### Text Cleaning

I had to do some cleaning of the text which I did in the code instead of manually. I started by making the whole file lower-case, then removing any punctuation and extra white space. I then had to add a list of names as these kept coming up in the results (makes sense as these are novels) but they wouldn't represent the language so I had to create a list of names to remove, which I had to hard-code.

### GUI

I moved on to implementing the ability to count occurances of the most common words and print them to the terminal which didn't look very nice. I then learned about the `:>` and `:<` function in Python and used it to format the output. However the interface didn't exist yet and after seeing a project use [BubbleTea](https://github.com/charmbracelet/bubbletea) (a terminal app framework for Go) I wanted to look for a Python library similar and [Questionary](https://github.com/tmbo/questionary/tree/master) was what I found. This is a really cool library for python terminal apps and was exactly what I was looking for, it's pretty and it's simple. I also ended up finding out about `rich`, a library for using some more advanced formatting for command line text. I used it mainly for colouring of text but it's good to know that this tool exists and there is good documentation of it.

### Saving and Reading Cards

I then moved on to the flashcard implementation as this was the main part of the project and the part I was looking forward to the least. I needed to be able to create, remove, edit, list and review the cards that were created. I started by making a very basic `Card` class that could store the word, meaning and an example. I then had to figure out how to store these cards for potential long-term use of the tool. I looked online and found `pickle`, a package for Python that could store Python objects neatly so I worked on getting the cards to store and read which was very easy with `pickle`.

## What I learned

- How to clean text better with the use of `.lower()`, `.translate()`, `.split()` and `.join()`
- The `counter` sub-class of `dicts` and how to use it (very basic level)
- How to use align text with the `:>` and `:<` operators
- About the python package `questionary` which I will likely use in future projects
- How to store data with the `pickle` package

## How can it be improved

- The use of `spaCy` (a natural language processing package) to remove names from the text instead of having a list of names hard-coded
- Improve the look with either a full GUI using a framework like `Tkinter` or `PyQt` or more advanced use of `rich`

## How to use

To run simply clone the rep and run:

```bash
pip install -r requirements.txt
```

Or sometimes on Windows you may need to run

```bash
py -m pip install -r requirements.txt
```

```bash
python3 Polish.py
```

This will run the program for you and you can navigate the menus using the arrow keys and enter to select. You should see a menu like this:

```
? What would you like to do?
>> Show most common words
   Search for a word (shows word in sentences)
   Flashcard mode
   Exit
```

The workflow of the tool is as follows:

```
├── Show most common words
│   └── How many words would you like to display?
│       └── Displays words
├── Search for a word
│   └── Input word (with accents)
│       └── Displays sentences
├── Flashcard mode (WIP)
│   ├── Create new cards
│   │   ├── Input word
│   │   ├── Input meaning
│   │   └── Input example
│   ├── Review cards (To-Do)
│   │   └── Runs a quiz of your cards
│   ├── List all cards
│   │   └── Shows all cards you have created
│   ├── Edit cards
│   │   └── Input card you want to edit
│   │       ├── Input word
│   │       ├── Input meaning
│   │       └── Input example
│   ├── Remove card
│   │   └── Input card you want to remove
│   ├── Remove all cards
│   └── Main menu
└── Exit
```
