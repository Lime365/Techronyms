import bs4
import os
import requests
import sqlite3

#make soup
url = 'https://techterms.com/category/acronyms'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
all = soup.findAll('tr')


#create file
file_path = 'c:/Users/Lime/pyProjects/tech_abs_quiz/'

acr = []
answer = []
merged = []


for i in all:
    ac = i.find('td')
    term = i.find_next('a')

    acr.append(ac)
    answer.append(term)

with open(file_path+'acronyms.txt', 'w+') as f:
    for id, line in enumerate(acr):
        f.write(str(id) +': '+str(line)+'\n')

with open(file_path+'acronyms.txt', 'r') as f:
    c = f.read()
    print(c)

with open(file_path+'terms.txt', 'w+') as f:
    for id, line in enumerate(answer):
        f.write(str(id)+': '+str(line)+'\n')
with open(file_path+'terms.txt', 'r') as f:
    c = f.read()
    print(c)

""" Takes the results from above,
removes the tags and then rewrites the text file"""

#For the acronyms
with open(file_path+'acronyms.txt', 'r') as f:
    c = f.readlines()

    better_ls = []
    for ac in list(c):
        start = ac.find('td')+3
        stop = ac.find('</td>')

        better_ls.append(ac[start:stop])
    print(c)
    print(better_ls)
better_ls.pop(0)
print(better_ls)

with open(file_path+'acronyms.txt', 'w+') as f:
    for i in better_ls:
        f.write(i+'\n')
with open(file_path+'acronyms.txt', 'r') as f:
    c = f.read()


with open(file_path+'terms.txt', 'r') as f:
    c = f.readlines()
    better_ls2 = []
    for i in c:
        start = i.find('>')+1
        stop = i.find('</')
        better_ls2.append(i[start:stop])

    better_ls2.pop(0)
    print(better_ls2)

with open(file_path+'terms.txt', 'w+') as f:
    for i in better_ls2:
        f.write(i+'\n')
