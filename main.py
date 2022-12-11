
print()
print("My Crypto App")
print()
print("1 - Top 100 sorted by market cap")
print("2 - Top 100 sorted by market cap")
print("3 - Top 100 sorted by market cap")
print("0 - Exit")
print()

choice = input("What is your choice(1-3): ")

sort = ""

if choice == '1':
    sort = 'market_cap'
if choice == '2':
    sort = 'percent_change_24h'
if choice == '3':
    sort = 'volume_24h'
if choice == '0':
    exit(0)

- name
- what is your portfolio
- make your choice