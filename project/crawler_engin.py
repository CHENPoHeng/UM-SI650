
import requests # use requests to crawl course data from UMICH schools' website
from bs4 import BeautifulSoup as bs # to clean and soup
import re
import csv

###### Engin
url = 'http://www.engin.umich.edu/college/academics/bulletin/courses'
r = requests.get(url)
soup = bs(r.text)

course_url = []
for i in soup.find_all("a", { "class" : "internal-link" })[1:]:
    i = i.get('href')
    course_url.append(i)

url = 'http://www.engin.umich.edu'

for i in course_url[0:1]:
    with open(i.split('/')[-1] + '_course_list.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['department', 'code', 'title', 'description', 'credit', 'advised_requisite', 'pre_requisite'])
        soup = bs(requests.get(url + i).text)
        unit = soup.title.text # get department name
        # code = [i.text.split('. ')[0] for i in soup.find_all('b')] # code
        titleList = [i.text.split('. ')[1] for i in soup.find_all('b')] # title
        # use title to find course information
        info = []
        for i in titleList:
            info.append([x for x in soup.find_all('p') if i in x.text][0])
        for i in info:
            tmp = i.b.text.split('. ')
            code = tmp[0]
            title = tmp[1].strip()
            desc = re.findall('<\/i>(.*?)<\/', i.encode('utf8'))[0].replace('<br/>','').strip()
            cred = re.findall(r'\((\d).*?\)', i.encode('utf-8'))[-1] if len(re.findall(r'\((\d).*?\)', i.encode('utf-8'))) > 0 else 0
            prea = 'NA'
            prep = re.split(r':|\s\(', i.i.text)[1] if len(re.split(r':|\s\(', i.i.text)) > 1 else re.split(r':|\s\(', i.i.text)[0]
            writer.writerow([unit, code, title, desc, cred, prea, prep])
