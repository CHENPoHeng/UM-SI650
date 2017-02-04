# -*- coding: utf-8 -*-

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

for i in course_url[14:]:
    with open('output/'+ i.split('/')[-1] + '_course_list.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['department', 'code', 'title', 'description', 'credit', 'advised_requisite', 'pre_requisite'])
        if re.match('^http:', i):
            soup = bs(requests.get(i).text)            
        else:
            soup = bs(requests.get(url + i).text)
        unit = soup.title.text # get department name
        print 'Now Working On:', unit 
        # code = [i.text.split('. ')[0] for i in soup.find_all('b')] # code
        if len(soup.find_all('b')) > 0:
            titleList = [i.text for i in soup.find_all('b')] # title
            flag = 'b'
        elif len(soup.find_all('strong')) > 0:
            titleList = [i.text for i in soup.find_all('strong')] # title
            flag = 'strong'
        # use title to find course information
        titleList = [i for i in titleList if len(i) > 5]
        info = []
        for i in titleList:
            info.append([x for x in soup.find_all('p') if i in x.text][0])
        for i in info:
            if flag == 'b':
                tmp = i.b.text
            elif flag == 'strong':
                tmp = i.strong.text
            tmp = re.findall('([\w\(\)\/\s]+\d{3}[\)|\s]*)[\s|\.](.*)', tmp)
            if len(tmp) == 0: continue
            code = tmp[0][0].strip()
            title = tmp[0][1].strip()
            if 'CEE 519. Hybrid and Composite Structures' in i.text: continue
            if 'CEE 621. Free Surface Flow' in i.text: continue
            if 'MacroSE 790. Faculty Activities Research Survey (1 credit)' in i.text: continue
            # if 'BIOMEDE 517 Neural Engineering' in i.text:
            #     tmp = tmp[0].split(' ')
            #     code = str(tmp[0])+' '+ str(tmp[1])
            #     title = str(tmp[2])+' '+ str(tmp[3])
            # elif 'CHE 500/CEE 500/ENSCEN 500 Environmental Systems and Processes' or 'CHE 559 (MATSCIE 559) (MACROMOL 559) Foundations of Nanotechnology II' in i.text:
            #     tmp = tmp[0].split(' ')
            #     code = str(tmp[0]) + ' ' + str(tmp[1]) + ' ' + str(tmp[2]) + ' ' + str(tmp[3])
            #     title = str(tmp[4]) + ' ' + str(tmp[5]) + ' ' + str(tmp[6]) + ' ' + str(tmp[7])
            # else: 
            #     code = tmp[0]
            #     title = tmp[1].strip()    
            if re.match('<\/i>(.*?)<\/', i.encode('utf8')):
                desc = re.findall('<\/i>(.*?)<\/', i.encode('utf8'))[0].replace('<br/>','').strip()
            elif re.match('<.*?>\s(.*?)<\/.*?>', i.encode('utf8')):
                desc = re.findall('<.*?>\s(.*?)<\/.*?>', i.encode('utf8'))[-1].replace('<br/>','').strip()
            elif len(re.findall('<.*?>\s(.*?)<\/.*?>', i.encode('utf8'))) == 0:
                desc = ''
            cred = re.findall(r'\((\d).*?\)', i.encode('utf-8'))[-1] if len(re.findall(r'\((\d).*?\)', i.encode('utf-8'))) > 0 else 0
            prea = 'NA'
            if i.i is not None:
                prep = re.split(r':|\s\(', i.i.text)[1].strip() if len(re.split(r':|\s\(', i.i.text)) > 1 else re.split(r':|\s\(', i.i.text)[0].strip()
            elif i.em is not None: 
                prep = re.split(r':|\s\(', i.em.text)[1].strip()
            else:
                prep = ''
            prep = prep.encode('utf-8')
            writer.writerow([unit.encode('utf-8'), code.encode('utf-8'), title.encode('utf-8'), desc, cred, prea.encode('utf-8'), prep])
