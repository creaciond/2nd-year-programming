import urllib.request
import re
import html
import codecs


def getPage(pageUrl):
    # try to access the page
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(pageUrl, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        page = response.read().decode('utf-8')
    return page


def cleanLines(text):
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    text = regTag.sub('', text)
    text = regSpace.sub('', text)
    text = html.unescape(text)
    return text


def getArticle(response, regex):
    articleText = ''
    if re.search(regex, response):
        articleHTML = re.search(regex, response).group(1)
        articleText = cleanLines(articleHTML)
        articleText = html.unescape(articleText)
    print(articleText)
    return articleText


def retrieveText(url):
    page = getPage(url)
    # regex for various sites
    regKP = re.compile('<div class=\"text\" itemprop=\"articleBody\" id=\"hypercontext\">(.*)?</div>')
    regSportsRu = re.compile('<div class=\"news-item__content js-mediator-article\">(.*)?</div>')
    regRSport = re.compile('<div class=\"b-article__text\">(.*)?</div>')
    regSpExpr = re.compile(
        '<div class=\"article_text publication blackcolor mt_30 mb_15 js-mediator-article\">(.*)?</div>')
    # "switch-case" for various sites
    article = ''
    if 'kp.ru' in url:
        article = getArticle(page, regKP)
    elif 'sports.ru' in url:
        article = getArticle(page, regSportsRu)
    elif 'sport-express.ru' in url:
        article = getArticle(page, regSpExpr)
    elif 'rsport.ru' in url:
        article = getArticle(page, regRSport)
    return article


def makeSet(text):
    wordSet = set()
    for word in text.split():
        word = word.strip('.,?!—\(-\)\[\]\"\'\«\»')
        word = word.lower()
        if word:
            wordSet.add(word)
    return wordSet


def doIntersections(sets):
    intersecRes = sets[0]
    for i in range(1, len(sets)):
         intersecRes = intersecRes.intersection(sets[i])
    intersecAr = list(sorted(intersecRes))
    with open('intersection.txt', 'w', encoding='utf-8') as f:
        line = '\r\n'.join(intersecAr)
        f.write(line)


def doSymDifferences(sets):
    uniqueSymDif = set()
    for eachSet in sets:
        for anotherSet in sets:
            symDifPart = set()
            if eachSet != anotherSet:
                symDifPart = eachSet.symmetric_difference(anotherSet)
                if symDifPart:
                    for each in symDifPart:
                        uniqueSymDif.add(each)
    with open('symmetricDifference.txt', 'w', encoding='utf-8') as f:
        line = '\r\n'.join(list(sorted(uniqueSymDif)))
        f.write(line)


def main():
    urls = ['http://www.kp.ru/daily/26615.7/3632101/', 'http://www.sports.ru/automoto/1046225660.html',
            'http://www.sport-express.ru/formula1/reviews/niko-rosberg-shokiroval-formulu-1-1072609/',
            'http://rsport.ru/auto/20161202/1113122367.html']
    sets = []
    for url in urls:
        text = retrieveText(url)
        sets.append(makeSet(text))
    doIntersections(sets)
    doSymDifferences(sets)


if __name__ == '__main__':
    main()
