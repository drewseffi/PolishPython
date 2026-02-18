# PolishPython

A simple Python command line tool for use in aiding Polish language learning. This tool uses public domain books taken from https://wolnelektury.pl/ as source material. This project is just a pet project and is not meant to be made for mass-use however I want to be able to track my progress and share it on GitHub.

## Features

- Count words in the text to show the most common words, very helpful for language learning flashcards
- Find sentences containing a selected word, good for finding out how words work in context of the language
- Flashcards built in 

## The Process

To start with I needed to find some source material for this project. Thankfully I was able to find [Wolne Lektury](https://wolnelektury.pl/) which hosts a lot of free, public domain books in the Polish language. I then had to manually copy and paste the full books into a text file `Books.txt`. I started with just two books but this grew over time to get better results.

I then had to do some cleaning of the text which I did in the code instead of manually. I started by making the whole file lower-case, then removing any punctuation and extra white space. I then had to add a list of names as these kept coming up in the results (makes sense as these are novels) but they wouldn't represent the language so I had to create a list of names to remove, which I had to hard-code.

I then implemented the ability to count occurances of the most common words and print them to the terminal which didn't look very nice. I then learned about the `:>` and `:<` function in Python and used it to format the output. However the interface didn't exist yet and after seeing a project use [BubbleTea](https://github.com/charmbracelet/bubbletea) (a terminal app framework for Go) I wanted to look for a Python library similar and [Questionary](https://github.com/tmbo/questionary/tree/master) was what I found. This is a really cool library for python terminal apps and was exactly what I was looking for, it's pretty and it's simple.

## What I learned

- How to clean text better with the use of `.lower()`, `.translate()`, `.split()` and `.join()`
- The `counter` sub-class of `dicts` and how to use it
- How to use align text with the `:>` and `:<` operators
- About the python package `questionary` which I will likely use in future projects

## How can it be improved

- The use of `spaCy` (a natural language processing package) to remove names from the text instead of having a list of names hard-coded

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
│   ├── Remove card (To-Do)
│   │   └── Input card you want to remove
│   ├── Remove all cards (To-Do)
│   └── Main menu
└── Exit
```
