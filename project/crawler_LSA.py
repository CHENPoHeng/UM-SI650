# -*- coding: utf-8 -*-

import requests # use requests to crawl course data from UMICH schools' website
from bs4 import BeautifulSoup as bs # to clean and soup
import re
import csv

#problem: invalid filename
#json type? =>solve different term ,same course
url = 'http://www.lsa.umich.edu/cg/cg_subjectlist.aspx?termArray=f_17_2160&termArray=su_17_2150&termArray=ss_17_2140&termArray=sp_17_2130&termArray=w_17_2120&termArray=f_16_2110&termArray=su_16_2100&termArray=ss_16_2090&termArray=sp_16_2080&termArray=w_16_2070&cgtype=gr'
r = requests.get(url)
soup = bs(r.text)
# html comtent
#prin"""t (r.text)

course_list_url = []
#print(soup.find_all("a",{ "target" : "_self" }))
dept_name =[]
for i in soup.find_all("a",{ "target" : "_self" })[1:]:
    if ":" not in i.text :
        dept_name.append(i.text)
        print ("text: "+i.text)
        i = i.get('href')    
        course_list_url.append(i)
    
    #print (i)


url = 'http://www.lsa.umich.edu/cg/'
for i in range(len(course_list_url)):      
    #dept_name[i] = re.sub(r'/?&?', '_', dept_name[i])
    with open('output/'+dept_name[i]+'.csv', 'w') as f:    
        # print (dept_name[i])    
        writer = csv.writer(f)
        writer.writerow(["department", "code", "title", "description", "credit", "advised_requisite","link"])
        # into inner page       
        r = requests.get(url+course_list_url[i])
        soup = bs(r.text)
        course_url = []    
        for j in soup.find_all("a",{ "target" : "_self" })[1:]:
            j = j.get('href')  
            #print (url+j)  
            link =  url+j        
            r_inner = requests.get(url+j)
            soup_inner = bs(r_inner.text)   

            # for  department,code,title 
            unit = soup_inner.title.text # get department name
            print (unit)
            if len(unit) ==0 :
                continue
            department=unit.split()[3]
            code=unit.split()[4]
            #title_g= re.search('(?<=-)\b(\w+)\b\|', unit)

            #title=title_g.group(0)
            title=unit[unit.find('-')+1:unit.rfind('|')]   
            # for credit & prerequisit
            content_table = soup_inner.find_all("div",{"id":"classDetailsBody"})
            credit=content_table[0].text.split( )[1]
            # if (i<2):
            #    print ("Credit: ",credit)
            description_list =  soup_inner.find_all("span",{"id":"contentMain_lblDescr"})
            description=description_list[0].text

            advised_requisite_list=soup_inner.find_all("span",{"id":"contentMain_lblAdvPre"})
            advised_requisite=""
            if (advised_requisite_list):
                advised_requisite=advised_requisite_list[0].text  

            if(i>1):
                print ('Now Working On:', department,code,title) 
                print ("Credit :", credit)
                print ("advised_requisite :", advised_requisite)
            writer.writerow([department.encode('utf-8'), code.encode('utf-8'), title.encode('utf-8'), description.encode('utf-8'), credit, advised_requisite.encode('utf-8'),link.encode('utf-8')])

