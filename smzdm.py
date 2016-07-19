from urllib import request
from bs4 import BeautifulSoup
import re,html5lib

def getLinks(inurl):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=inurl, headers=headers)
    html = request.urlopen(req)
    baseObj=BeautifulSoup(html,'html5lib')
    
    return baseObj
pages=list()
for pageNum in range(3,7):
    indexurl="http://www.smzdm.com/mall/amazon_cn/youhui/p"+str(pageNum)+"/"
    SMZDMlist=getLinks(indexurl).find_all('a',{'target':'_blank','class':'picBox'})
    for link in SMZDMlist:
        if 'href' in link.attrs:
             newPage=link.attrs['href']
             #print(newPage)
             pages.append(newPage)
             
urltime=dict()
for url in pages:
    amazonlist=getLinks(url)
    url=amazonlist.find('a',{'itemprop':"url",'class':"pic-Box",'target':"_blank"})
    amazonurl=url.attrs['href']
    timet=re.compile(r'时间：[0-9-: ]+')
    timeattr=amazonlist.find('span',text=timet)
    time=timeattr.get_text()[3:]
    urltime[amazonurl]=time

    
for asinurl in urltime.keys():
    asinhtml=getLinks(asinurl).script.get_text()
    s=re.compile(r'\|B[0-9a-zA-Z]{9}\|')
    asin=re.search(s,asinhtml)
    if asin is not None:
        print('%-12s %s' %(urltime[asinurl],asin.group()[1:11]))
    
    
    
    
    
    
