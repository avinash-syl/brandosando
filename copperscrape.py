import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base_url = "https://www.coppermind.net"
char_url = "/wiki/Category:Characters"
page = requests.get(f"{base_url}{char_url}")

soup = BeautifulSoup(page.content, "html.parser")

characters = {}
for letter in soup.find_all('div', {"class": "mw-category-group"})[13:]:
    for character in letter.find_all('a', href=True):
        characters[character.text] = character['href']
            
# print(characters)

final_characters = pd.DataFrame(columns=["name", "books", "world", "groups", "universe"])
for character in characters:
    url = f"{base_url}{characters[character]}"
    print(url)
    char_page = requests.get(url)
    char_soup = BeautifulSoup(char_page.content, "html.parser")
    books = 'Entity'
    universes = 'Independent'
    world = 'Unknown'
    groups = 'NA'
    
    info_table = char_soup.find_all('table', {'class': 'infobox side'})[0]
    # Getting books the character appears in
    for f in info_table.find_all('th', string=re.compile('Featured In')):
        if len(f)>0:
            books = f"{','.join([x.text if x is not None else 'Entity' for x in f.parent.find_all('a', href=True)])}"
            
    # Getting universes the character appears in
    for u in info_table.find_all('th', string=re.compile('Universe')):
        if len(u)>0:
            universes = f"{','.join([x.text if x is not None else 'Independent' for x in u.parent.find_all('a', href=True)])}"

    # Getting world from which character originates
    for w in info_table.find_all('th', string=re.compile('World')):
        if len(w)>0:
            world = f"{','.join([x.text if x is not None else 'Unknown' for x in w.parent.find_all('a', href=True)])}"
            
    # Getting groups character is associated with
    for g in info_table.find_all('th', string=re.compile('Groups')):
        print(g)
        if len(g)>0:
            groups = f"{','.join([x.text if x is not None else 'NA' for x in g.parent.find_all('a', href=True)])}"
    
    info = [character, books, world, groups, universes]
    print(info)
    final_characters.loc[len(final_characters)] = info

print(final_characters.info())
final_characters.to_csv('copper_chars.csv', sep=',', encoding='utf-8')