# PolishPython 🇵🇱

A simple Python command line tool for use in aiding Polish language learning. This tool uses public domain books taken from https://wolnelektury.pl/ as source material. This project is just a pet project and is not meant to be made for mass-use however I want to be able to track my progress and share it on GitHub.

## Features
- Count words in the text to show the most common words, very helpful for language learning

## The Process

To start with I needed to find some source material for this project. Thankfully I was able to find [Wolne Lektury](https://wolnelektury.pl/) which hosts a lot of free, public domain books in the Polish language. I then had to manually copy and paste the full books into a text file `Books.txt`. I started with just two books but this grew over time to get better results.

I then had to do some cleaning of the text which I did in the code instead of manually. I started by making the whole file lower-case, then removing any punctuation and extra white space. I then had to add a list of names as these kept coming up in the results (makes sense as these are novels) but they wouldn't represent the language so I had to create a list of names to remove, which I had to hard-code.

I then implemented the ability to count occurances of the most common words and print them to the terminal which didn't look very nice.

## What I learned
- How to clean text better with the use of `.lower()`, `.translate()`, `.split()` and `.join()`
- The `counter` sub-class of `dicts` and how to use it
- How to use align text with the `:>` and `:<` operators

## How can it be improved

- The use of `spaCy` (a natural language processing package) to remove names from the text instead of having a list of names hard-coded

## How to use

To run simply clone the rep and run:

`pip install -r requirements.txt`
`python3 Polish.py`