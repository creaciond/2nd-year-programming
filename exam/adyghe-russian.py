import re
import html


def cleanText(text):
    text = html.unescape(text)
    regTag = re.compile('<.*?>', flags = re.DOTALL)
    regSpace = re.compile('\s{2,}', flags = re.DOTALL)
    text = regTag.sub('', text)
    text = regSpace.sub('', text)
    return text


def retrieveArticleWords(articlePath):
    with open(articlePath, 'r', encoding='utf-8') as f:
        # get words
        content = f.read()
        regArticle = re.compile('<p>(.*)?</p>')
        allText = ' '.join(re.findall(regArticle, content))
        allText = cleanText(allText)
        words = allText.lower().split()
        # get rid of numbers, numerals, etc
        regNum = '[0-9]+'
        actualWords = set()
        for word in words:
            word = word.strip('.,?!:;\'\"-«»—')
            if (not re.search(regNum, word)) and (word not in actualWords) and word:
                actualWords.add(word)
    return actualWords


def retrieveUnparsedWords(unparsedPath):
    unparsedWords = set()
    with open(unparsedPath, 'r', encoding='utf-8') as f:
        # each line == new word
        for word in f.readlines():
            if word not in unparsedWords:
                unparsedWords.add(word.strip('\n'))
    return unparsedWords


def intersectingWords(article, unparsed):
    intersection = article & unparsed
    line = '\n'.join(list(sorted(intersection)))
    with open('wordlist.txt', 'w', encoding='utf-8') as f:
        f.write(line)


def main():
    articlePath = 'adyghePolitics.htm'
    unparsedPath = 'adyghe-unparsed-words.txt'
    articleWords = retrieveArticleWords(articlePath)
    unparsedWords = retrieveUnparsedWords(unparsedPath)
    # задание на 5
    intersectingWords(articleWords, unparsedWords)


if __name__== '__main__':
    main()