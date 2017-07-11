#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
from sys import argv
import re

#applying commands in terminal
GREEN = '\033[92m'
BOLD = '\033[1m'

command =argv[1]
#extracting first link from google

def tgs(soup):
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
        if tag.name==h_tag.name   :
            print(BOLD+tag.get_text())
        tag=tag.next_sibling
def lifewire(link):
    r=requests.get(link)
    soup=bs(r.content,'html.parser')   
    for block in soup.find_all('blockquote'):
        print(BOLD+block.find_previous_sibling('h3').string)
        print(GREEN+block.get_text())
g_url='https://www.google.com/search?q={}+command+examples&gbv=1&sei=YwHNVpHLOYiWmQHk3K24Cw'.format(command)
g_page=requests.get(g_url)
print(g_url)
g_soup=bs(g_page.content,'html.parser')
count=0
while(count<4):
    g_tag=g_soup.find_all('h3')[count]
    text=g_tag.get_text()

    link=g_tag.a['href'][7:g_tag.a['href'].index('&')]
    print(link)
    print(text)
    print(count)
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




