# coding:utf-8

from selenium import webdriver
from urllib import quote
from urllib2 import Request,urlopen
from bs4 import BeautifulSoup

def createUrl(company):
    qcompany=quote(company)
    url='http://www.tianyancha.com/search/'+qcompany
    return url

def makeDriver(url) :
    driver = webdriver.PhantomJS()
    driver.get(url)
    return driver

def findCompany(company):
    aurl=createUrl(company)
    driver=makeDriver(aurl)
    element=driver.find_element_by_class_name("query_name")
    companyname=element.find_element_by_class_name("ng-binding").text
    if companyname==company.decode("utf-8"):
        realurl=element.get_attribute('href')
    driver.quit()
    return realurl

'''def getShareholders(company):
    url=findCompany(company)
    print url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req=Request(url=url,headers=headers)
    html=urlopen(req)
    baseObj=BeautifulSoup(html)
    print baseObj'''

def getShareholders(company):
  
    r=findCompany(company)
    print r
    driver=makeDriver(r)
    holders=driver.find_elements_by_class_name("ng-scope")
    for holder in holders:
        if holder.get_attribute('ng-repeat')=="investor in company.investorList track by $index":
            hname=holder.find_element_by_tag_name('a').text.encode('utf-8')
            money=holder.find_element_by_css_selector('p.ng-binding').text.encode('utf-8')
            print '%s\t%s\t%s'%(company,hname,money)
    driver.quit()

def main():
    f=open('companies.txt','r')
    for company in f.readlines():
        company=company.rstrip()
        try:
            getShareholders(company)
        except:
            pass
    f.close()
      
if __name__=='__main__':
    global realurl
    main()

