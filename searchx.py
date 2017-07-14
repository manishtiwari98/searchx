#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import sys
import re,os

#applying commands in terminal
GREEN = '\033[92m'
BOLD = '\033[1m'

command =sys.argv[1]

if os.path.exists('./'+command):
    os.system('less -R '+command)
    exit()

tmp=open(command,'w')
sys.stdout=tmp

data=0
def tgs(soup):
    global data
    for heading in soup.find_all(re.compile('^h[2-5]$')):
        if heading.get_text().startswith('1.'):
            tag=h_tag=heading
            break
        else :
            tag=0
    print(" "*20+BOLD+"Frequently used "+command+" commands"+"\n"*2)
    while(tag):
        if tag.name=='pre' :
            if tag.script:
                tag.script.decompose()
            if tag.strong and tag.strong.a:
                tag.strong.a.decompose()
            print( '\n'.join(GREEN + line for line in tag.get_text().split('\n')))
            print('-'*20+'\n')
            data=1
        if tag.name==h_tag.name   :
            print(BOLD+tag.get_text())
        tag=tag.next_sibling

def lifewire(link):
    global data
    r=requests.get(link)
    soup=bs(r.content,'html.parser')   
    print(" "*20+BOLD+"Frequently used "+command+" commands"+"\n"*2)
    for block in soup.find_all('blockquote'):
        print(BOLD+block.find_previous_sibling('h3').string)
        print(GREEN+block.get_text())
        data=1
#extracting first 3 link from goole results
g_url='https://www.google.com/search?q={}+command+examples&gbv=1&sei=YwHNVpHLOYiWmQHk3K24Cw'.format(command)
g_page=requests.get(g_url)
g_soup=bs(g_page.content,'html.parser')
count=0
links=[]
while(count<4):
    g_tag=g_soup.find_all('h3')[count]
    text=g_tag.get_text()
    link=g_tag.a['href'][7:g_tag.a['href'].index('&')]
    links.append(link)
    if all(val in text.lower() for val in ['example', command]):
        if re.findall(r'(thegeekstuff|tecmint)',link.lower()):
            r=requests.get(link)
            soup=bs(r.content,'html.parser')
            tgs(soup)
            break
        if re.findall(r'(lifewire)',link.lower()):
            lifewire(link)
            break
        count+=1
    else:
        count+=1
tmp.close()
sys.stdout=sys.__stdout__
if count==4 or not data:
    os.system('rm '+command)
    print("Command You entered is not available right now.")
    print("Following are few links related to your command. Pls select the number.")
    index=1
    for link in links:
        print(str(index)+". "+link)
        index+=1
    print("5. man page")
    x=int(input("Select the link number or man page:"))
    if(x==5):
        os.system('man '+command)
    elif(x in range(1,5)):
        os.system("firefox "+links[x-1])
    else:print("Wrong Input")
    exit()

os.system('less -R '+command)
if not 'save' in sys.argv:
    os.system('rm '+command)
