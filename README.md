# Dictionary-Random-and-Online-Attack
Demonstrates a dictionary attack, random attack and online attack.
The word list used was from github.com/AllenDowny. 

## accounts_dictionary.txt
List with usernames, salts and passwords hashed using hash256 and hash1 encryption. Salt was added after the word before hashing. Account names were made up along with passwords. This file is used in the dictionary attack.

## accounts_random.txt
List with usernames and passwords hashed using hash256 and hash1 encryption. This file is used in the random attack.

## MultAttacker.py
Python 3 file that has the following methods:
    hashing1    - hash1 encryption for strings.
    hashing256  - hash256 encryption for strings.
    dictionary_reader - reads word list and accounts_dictionary.txt.
    dictionary_attack - initiates dictionary attack.
    random_reader - reads accounts_random.txt
    random_characters - generates all possible combinations of letters up to a 10 letter word.
    random_attack - initiates random attack.
    online_attack - connects to a website and attempts a two letter password attempt each second.
    main  - runs all methods.
Running the random attack with random_characters may cause issues with memory. Run only one of letter combination at a time to avoid this issue.
    
