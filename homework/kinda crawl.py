# Максимова Дарья, БКЛ153
import urllib.request
import re
import os
import time


def crawl(pageUrl):
    time.sleep(2)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
    return page

def getPages(pageUrl):
    # try to access the page
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
    return page


def getAddresses():
    for i in range(1,2):
        mainUrl = 'http://polkrug.ru/news?p=' + str(i)
        print(mainUrl)
        response = getPages(mainUrl)
        regLink = re.compile('<h3>\r\n.*?\"(.*)?\"')
        for line in response:
            if re.search(regLink, line):
                articleUrl = regLink.group(1)
                normUrl = 'http://polkrug\.ru' + articleUrl
                print(normUrl)

def main():
   getAddresses()


if __name__ == '__main__':
    main()
