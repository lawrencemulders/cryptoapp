from coincap_global import *
from coincap_listings import *
from coincap_quotes import *
from top100 import *
from crypto_portfolio import *
from alerttracking import *

print()
print("Welcome to cryptoapp")
print()
name = input("What is your name?")

print("Hi " + name + "! ")
print()
print("1 - Generic Overview of the Cryptocurrency Market")  # coincap_global
print("2 - List of all Cryptocurrencies")  # coincap_listings
print("3 - Search a Specific Cryptocurrency")  # coincap_quotes
print("4 - Top 100 Cryptocurrency Per Filter")  # top100
print("5 - Your Portfolio")  # crypto_portfolio
print("6 - Alert Tracking of Your Cryptocurrencies")  # alerttracking
print("0 - Exit")
print()
choice = input("What is your choice(1-6)? ")

if choice == '1':
    cryptoglobal()
if choice == '2':
    cryptolistings()
if choice == '3':
    cryptoquotes()
if choice == '4':
    top100()
if choice == '5':
    user_input = input(
        "Please provide your portfolio as a csv. First column is the ticker and the second should contain the "
        "quantity per ticker")
    cryptoportfolio(user_input)
if choice == '6':
    user_input = input(
        "Please provide your portfolio as a csv. First column is the ticker and the second should contain the "
        "quantity per ticker")
    alerttracking(user_input)
if choice == '0':
    exit(0)
