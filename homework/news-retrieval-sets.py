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


def cleanLines(text):
    regTag = re.compile('<.*?>')
    regSpace = re.compile('\s{2,}')
    text = regTag.sub('', text)
    text = regSpace.sub('', text)        
    text = html.unescape(text)
    return text


def getArticle(response, regex):
	if re.search(regex, response):
		articleHTML = re.search(regex, response).group(1)
		articleText = cleanLines(articleHTML)
		articleText = html.unescape(article)
		print(articleText)


def retrieveText(url):
	page = getPage(url)
	# regex for various sites
	regKP = re.compile('<div class=\"text\" itemprop=\"articleBody\" id=\"hypercontext\">(.*)?</div>')
	regSportsRu = re.compile('<div class=\"news-item__content js-mediator-article\">(.*)?</div>')
	regRSport = re.compile('<div class=\"b-article__text\">(.*)?</div>')
	regSpExpr = re.compile('<div class=\"article_text publication blackcolor mt_30 mb_15 js-mediator-article\">(.*)?</div>')
	# "switch-case" for various sites
	if 'kp.ru' in url:
		article = getArticle(page, regKP)
	elif 'sports.ru' in url:
		arctile = getArticle(page, regSportsRu)
	elif 'sport-express.ru' in url:
		article = getArticle(page, regSpExpr)
	elif 'rsport.ru' in url:
		article = getArticle(page, regRSport)
	


def main():
	urls = ['http://rsport.ru/auto/20161202/1113122367.html', 'http://www.kp.ru/daily/26615.7/3632101/', 'http://www.sports.ru/automoto/1046225660.html', 'http://www.sport-express.ru/formula1/reviews/niko-rosberg-shokiroval-formulu-1-1072609/']
	for url in urls:
		retrieveText(url)		


if __name__ == '__main__':
	main()
