# Максимова Дарья, БКЛ153
# coding = utf-8
import urllib.request
import re
import os
import html


def getPage(pageUrl):
    # try to access the page
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
    return page


def deleteTags(lines):
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    newLines = []
    for line in lines:
        line = regTag.sub('', line)
        line = regSpace.sub('', line)
        newLines.append(line)
    return newLines


def cleanLines(lines):
    lines = deleteTags(lines)
    for line in lines:
        line = html.unescape(line)
        print(line)


def getText(response):
    # bunch of regex for everything
    regFirst = re.compile('<p><strong>.*?</strong></p>')
    regBlock = re.compile('<p>[А-ЯЁ].*?</p>')
    # search for text
    firstline = regFirst.findall(response)
    text = regBlock.findall(response)
    # clean and print the text
    firstline = cleanLines(firstline)
    text = cleanLines(text)


def getHeader(response):
    regHeader = re.compile('<h1>.*?</h1>')
    headers = regHeader.findall(response)
    headers = cleanLines(headers)
    return headers 
        

def getDate(response):
    # regex
    regDate = re.compile('<div class="news_date">(.*)?</div>')
    # search
    for line in response:
        if re.search(regDate, line):
            date = regDate.group(1)
    # edit format
    months = {'января':'01', 'февраля':'02', 'марта':'03', 'апреля':'04', 'мая':'05', 'июня':'06',
              'июля':'07', 'августа':'08', 'сентября':'09', 'октября':'10', 'ноября':'11', 'декабря':'12'}
    dateParts = date.split(' ')
    for month in months:
        if month in dateParts[1]:
            dateParts[1] = months[month]
    if len(dateParts[0]) == 1:
        dateParts[0] = '0' + dateParts[0]
    newdate = '.'.join(dateParts)
    return newdate


def getAuthor(response):
    # regex
    regAuthor = re.compile('<div><span class="article_about">Текст:</span><span class="author_fio">(.*)?</span></div>')
    # search
    for line in response:
        if re.search(regAuthor, line):
            author = regAuthor.group(1)
    return author


def getTopic(response):
    # <a class="rubric"
    regTopic = re.compile('<a class="rubric".*?>(.*)?<')
    for line in response:
        if re.search(regTopic, line):
            return regTopic.group(1)
        

def getAddresses():
    for i in range(1,2):
        mainUrl = 'http://polkrug.ru/news?p=' + str(i)
        print(mainUrl)
        response = getPage(mainUrl)
        regLink = re.compile('<h3>\r\n.*?\"(.*)?\"')
        for line in response:
            if re.search(regLink, line):
                articleUrl = regLink.group(1)
                normUrl = 'http://polkrug\.ru' + articleUrl
                print(normUrl)


def getAddresses(pageNum):
    mainUrl = 'http://polkrug.ru/news?p=' + pageNum
    print(mainUrl)
    response = getPages(mainUrl)
    urls = []
    regLink = re.compile('<h3>\r\n.*?\"(.*)?\"')
    for line in response:
        if re.search(regLink, line):
            articleUrl = regLink.group(1)
            normUrl = 'http://polkrug\.ru' + articleUrl
            print(normUrl)
            urls.append(normUrl)
    return urls


def parsePage():
    pageUrl = 'http://polkrug.ru/news/gorod/sobytie/5265-shagaem-po-strane'
    response = getPage(pageUrl)
    text = ''
    text += '@au ' + getAuthor(response) + '\r\n'
    text += '@ti ' + getHeader(response) + '\r\n'
    date = getDate(response)
    text += '@da ' + date + '\r\n'
    text += '@topic ' + getTopic(response) + '\r\n'
    text += '@url ' + pageUrl + '\r\n'
    text.append(getText(response))
    # decide where to put the text
    dateParts = date.split(' ') 
    return text, dateParts[1], dateParts[2]


def savePage(text, month, year):
    directory = 'plain' + os.sep + year + os.sep + month
    if not os.path.exists(directory):
		os.makedirs(directory)
	num = len(os.listdir(directory)) + 1
	filename = directory + 'article' + str(num) + '.txt'
	file = open(filename, 'w', encoding='utf-8')
	file.write(text)
	file.close()


def main():
    for i in range(1,300):
        pageUrls = getAddresses(str(i))
        for eachUrl in pageUrls:
            text, month, year = parsePage(eachUrl)
            savePage(text, month, year)
            


if __name__ == '__main__':
    main()
