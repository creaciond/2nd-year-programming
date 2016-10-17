# Максимова Дарья, БКЛ153
# coding: utf-8
import urllib.request
import re
import os
import html
import time


def getPage(pageUrl):
    # try to access the page
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(pageUrl, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
    return page

#             == Text processing ==

#def deleteTags(lines):
    #regTag = re.compile('<.*?>')
    #regSpace = re.compile('\s{2,}')
    #newLines = []
    #for line in lines:
        #line = regTag.sub('', line)
        #line = regSpace.sub('', line)
        #newLines.append(line)
    #return newLines


def cleanLines(lines):
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    newLines = []
    for line in lines:
        line = regTag.sub('', line)
        line = regSpace.sub('', line)        
        line = html.unescape(line)
        newLines.append(line)
    return newLines


def getText(response):
    # bunch of regex for everything
    regFirst = '<p><strong>.*?</strong></p>'
    regBlock = '<p>(?:[А-ЯЁ]|&).*?</p>'
    paragraphs = []
    # search for text
    firstline = re.findall(regFirst, response)
    paragraphs = re.findall(regBlock, response)
    # clean and print the text
    firstline = cleanLines(firstline)
    paragraphs = cleanLines(paragraphs)
    text = []
    text.append(firstline)
    text1 = ''
    for line in paragraphs:
        text.append(line)
        text1 = text1 + line + '\r\n'
    return text1


#             == Retrieving info from article == 
def getHeader(response):
    header = ''
    regHeader = '<h1>(.*)?</h1>'
    resHeader = re.search(regHeader, response)
    if resHeader:
        header = resHeader.group(1)
    return header


def getAuthor(response):
    author = ''
    # regex
    regAuthor = re.compile('<div><span class=\"article_about\">Текст:</span><span class=\"author_fio\">(.*)?</span></div>')
    # search
    resAuthor = re.search(regAuthor, response)
    if resAuthor:
        author = resAuthor.group(1)
        authorParts = author.split(' ')
        for part in authorParts:
            part = part[0] + part[1:].lower()
        author = ' '.join(authorParts)
    return author


def getDate(response):
    date = ''
    # regex
    regDate = 'class=\"news_date\">(.*?)<'
    # search
    resDate = re.search(regDate, response)
    if resDate:
        date = resDate.group(1)
    # edit format
    months = {'января':'01', 'февраля':'02', 'марта':'03', 'апреля':'04', 'мая':'05', 'июня':'06', 'июля':'07', 'августа':'08', 'сентября':'09', 'октября':'10', 'ноября':'11', 'декабря':'12'}
    dateParts = date.split(' ')
    for month in months:
        if month in dateParts[1]:
            dateParts[1] = months[month]
    if len(dateParts[0]) == 1:
        dateParts[0] = '0' + dateParts[0]
    newdate = '.'.join(dateParts)
    return newdate


def findPath(date):
    dateParts = date.split('.')
    # 0 - date, 1 - month, 2 - year
    return dateParts[1], dateParts[2]


def getTopic(response):
    topic = ''
    regTopic = re.compile('<a class="rubric".*?>(.*)?</a>')
    resTopic = re.search(regTopic, response)
    if resTopic:
        topic = resTopic.group(1)
    return topic

        
#             == web crowler ==
def getAddresses():
    urls = []
    for i in range(1,2):
        # time.sleep(2)
        mainUrl = 'http://polkrug.ru/news?p=' + str(i)
        response = getPage(mainUrl)
        lines = response.split('>')
        regLink = re.compile('a class=\"more_link\" href=\"(.*?)\"')
        for line in lines:
            hasLink = re.search(regLink, line)
            if hasLink:
                articleUrl = hasLink.group(1)
                normUrl = 'http://polkrug.ru' + articleUrl
                urls.append(normUrl)
    return urls


#            == title for txt ==
def getTitle(pageUrl):
    response = getPage(pageUrl)
    title = ''
    title += '@au ' + getAuthor(response) + '\r\n'
    title += '@ti ' + getHeader(response) + '\r\n'
    title += '@da ' + getDate(response) + '\r\n'
    title += '@topic ' + getTopic(response) + '\r\n'
    title += '@url ' + pageUrl + '\r\n\r\n'
    return title


#             == save text ==
def savePage(textar, title, month, year):
    directory = '.' + os.sep + 'plain' + os.sep + year + os.sep + month
    if not os.path.exists(directory):
        os.makedirs(directory)
    num = len(os.listdir(directory)) + 1
    filename = directory + os.sep + 'article' + str(num) + '.txt'
    file = open(filename, 'w', encoding='utf-8')
    file.write(title)
    for line in textar:
        file.write(line)
    file.close()
    return 'article' + str(num) + '.txt'


#             == mystem parsing==
def stemPage(pageFolder, pageFilename):
    mystem = '/Users/dariamaximova/Desktop/HSE/programming/hse-coding-2/homework/mystem'
    sourceDir = '.' + os.sep + 'plain' + os.sep + pageFolder + os.sep + pageFilename
    goalDir = '.' + os.sep + 'mystem-plain' + os.sep + pageFolder
    if not os.path.exists(goalDir):
        os.makedirs(goalDir)
    # mystem-plain
    mystem_plain = mystem + ' ' + sourceDir + ' ' + goalDir + os.sep + pageFilename + ' -cid --format text'
    os.system(mystem_plain)
    # mystem-xml
    goalDir = '.' + os.sep + 'mystem-xml' + os.sep + pageFolder
    if not os.path.exists(goalDir):
        os.makedirs(goalDir)
    mystem_xml = mystem + ' ' + sourceDir + ' ' + goalDir + os.sep + pageFilename + ' -cid --format xml'
    os.system(mystem_xml)


#             == add metadata ==
def meta(path, author, date, url, year):
    tablePath = 'metadata.csv'
    if not os.path.isfile(tablePath):
        create = open(tablePath, 'w', encoding='utf-8')
        create.close()
    table = open(tablePath, 'a', encoding='utf-8')
    infoString = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрегиональная\t%s\tПолярный круг\t\t%s\tгазета\tРоссия\tЯмало-Ненецкий автономный округ\tru'
    text = getText(url)
    header = getHeader(text)
    topic = getTopic(text)
    table.write(infoString % (path, author, header, date, topic, url, year) + '\r\n')
    table.close()


def main():
    pageUrls = getAddresses()
    i = 1
    for pageUrl in pageUrls:
        page = getPage(pageUrl)
        text = getText(page)
        date = getDate(page)
        auth = getAuthor(page)
        month, year = findPath(date)
        title = getTitle(pageUrl)
        # first save: no title, for parsing via mystem
        pageFile = savePage(text, '', month, year)
        pageFolder = year + os.sep + month
        # parsing
        stemPage(pageFolder, pageFile)
        # writing metadata
        plainPath = pageFolder + os.sep + pageFile
        meta(plainPath, auth, date, pageUrl, year)
        print(i)
        i += 1
        


if __name__ == '__main__':
    main()
