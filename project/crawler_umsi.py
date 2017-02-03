
import requests # use requests to crawl course data from UMICH schools' website
from bs4 import BeautifulSoup as bs # to clean and soup
import re

###### UMSI
url = 'https://www.si.umich.edu/programs/courses/catalog'
r = requests.get(url)

soup = bs(r.text)
course_url = []

for i in soup.find_all('a'):
    i = i.get('href')
    if i is not None and '/programs/courses/' in i:
        course_url.append(i)

url = 'https://www.si.umich.edu'

with open('umsi_course_list.txt', 'w') as f:
    for i in set(course_url):
        soup = bs(requests.get(url + i).text)
        unit = soup.h1.text
        tmp = soup.find("h1", { "class" : "title" }).text
        code = tmp.split(':')[0].replace(' ', '')
        name = tmp.split(':')[1].strip()
        desc = soup.find("p", { "class" : "course2desc" }).text.strip()
        cred = soup.find("div", { "class" : "course2credit" }).text.split(':')[1].strip()
        prea = soup.find("div", { "class" : "course2prea" }).text.split(':')[1].strip()
        prep = soup.find("div", { "class" : "course2prer" }).text.split(':')[1].strip()
        f.write('{}, {}, {}, {}, {}, {} \n'.format(unit, name, desc, cred, prea, prep))
