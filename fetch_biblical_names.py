import requests
import re
import string


names_regex = re.compile(r'<li>.+?title=".+?">([\w-]+?)<')

names = []

for letter in string.ascii_uppercase:
    response = requests.get("https://en.wikipedia.org/wiki/List_of_biblical_names_starting_with_" + letter).text
    names += names_regex.findall(response)
    print(letter, "loaded", len(names_regex.findall(response)), "names")

names = [i for i in names if i not in ['ISBN', 'redirect']]

with open("res/names.txt", "w+") as f:
    for name in names:
        f.write(name + "\n")
