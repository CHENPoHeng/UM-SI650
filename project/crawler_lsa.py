import requests # use requests to crawl course data from UMICH schools' website
from bs4 import BeautifulSoup as bs # to clean and soup
import re
import csv

url = 'http://www.lsa.umich.edu/cg/cg_subjectlist.aspx?termArray=f_17_2160&termArray=su_17_2150&termArray=ss_17_2140&termArray=sp_17_2130&termArray=w_17_2120&termArray=f_16_2110&termArray=su_16_2100&termArray=ss_16_2090&termArray=sp_16_2080&termArray=w_16_2070&cgtype=ug'
soup = bs(requests.get(url).text)

subjects_url_name = {}

table = soup.find_all("tbody")
subjects = table[0].find_all("tr")

url = 'http://www.lsa.umich.edu/cg/'
# Get subject urls
for sub in subjects:
	# Only keep those highlighted in bold
	sub = sub.find('td', {'style':'width:150px;'})
	if sub != None:
		sub = sub.find('a')
		sub_name = sub.text
		sub = sub.get('href')
		subjects_url_name[url+sub] = sub_name

# idx = 0
# for sub_url, name in subjects_url_name.items():
#     idx += 1
#     if idx == 1:
#     	break

# Go into subject and find all classes
for sub_url, sub_name in subjects_url_name.items():
	soup = bs(requests.get(sub_url).text)
	classes = soup.find_all("div",{"class":"row toppadding_main bottompadding_interior"})
	with open('output/' + sub_name + '_course_list.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['department', 'subject', 'code', 'title', 'credits', 'description'])
		# TODO: this is a for loop
	for c in classes:
		c = classes[0]
		c = c.find('a')
		# Here c is a relative path
		c = url + c.get('href')
		soup = bs(requests.get(c).text)
		class_title  = soup.title.text # get the class title
		subject = soup.find('span', {'id':'contentMain_lblSubjectDescr'}).text
		code = re.findall('(\w+\s\d{3})\s-\s(.*?)\|\s\w+\s\d+', class_title)[0][0]
		title = re.findall('(\w+\s\d{3})\s-\s(.*?)\|\s\w+\s\d+', class_title)[0][1]
		department = soup.find('span', {'id':'contentMain_lblDeptDescr'}).text
		description = soup.find('span', {'id':'contentMain_lblDescr'}).text
		credits = soup.find('span', {'id':'contentMain_lblCredits'}).text
		writer.writerow([department.encode('utf-8'), subject.encode('utf-8'), code.encode('utf-8'), title.encode('utf-8'), credits.encode('utf-8'), description.encode('utf-8')])
		print('Now working on subject: ' + sub_name + ', class: ' + title)