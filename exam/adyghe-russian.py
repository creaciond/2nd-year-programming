import re
import html
import os


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


def doMystem(unparsedPath):
    mystemPath = '/Users/dariamaximova/Desktop/HSE/Программирование/mystem'
    sourcePath = '.' + os.sep + unparsedPath
    goalPath = '.' + os.sep + 'mystemRes.txt'
    # options: input to output, English grammemes
    options = '-cdi --eng-gr'
    mystemCommand = mystemPath + ' ' + sourcePath + ' ' + goalPath + ' ' + options
    os.system(mystemCommand)
    return goalPath


def detectRusNouns(unparsedPath):
    # parsingResult = doMystem(unparsedPath)
    parsingResult = '.' + os.sep + 'mystemRes.txt'
    wannabeRusNouns = set()
    with open(parsingResult, 'r', encoding='utf-8') as f:
        regSNom = 'S[a-z,=]*?(nom,sg)'
        for parsing in f.readlines():
            if '?' not in parsing:
                if re.search(regSNom, parsing):
                    # parsing.split('{')[0] == word in Adyghe
                    if (parsing.split('{')[0] not in wannabeRusNouns) and (not parsing.split('{')[0].startswith('ӏ')):
                        wannabeRusNouns.add(parsing.split('{')[0])
    with open('rus_nouns.txt', 'w', encoding='utf-8') as f:
        line = '\n'.join(list(sorted(wannabeRusNouns)))
        f.write(line)
    return wannabeRusNouns


def makeInserts(wannabeRusNouns, mystemPath):
    inserts = set()
    with open(mystemPath, 'r', encoding='utf-8') as f:
        for parsing in f.readlines():
            adygheWord = parsing.split('{')[0]
            if adygheWord in wannabeRusNouns:
                regRusLemma = '(.*?)='
                hasRusLemma = re.search(regRusLemma, parsing.split('{')[1])
                regSNom = 'S[a-z,=]*?(nom,sg)'
                isSNom = re.search(regSNom, parsing.split('{')[1])
                if hasRusLemma and isSNom:
                    rusLemma = re.search(regRusLemma, parsing.split('{')[1]).group(1)
                    insertSQL = 'INSERT INTO rus_words (wordform, lemma) VALUES \"%s\", \"%s\"' % (adygheWord, rusLemma)
                    if insertSQL not in inserts:
                        inserts.add(insertSQL)
    with open('sql.txt', 'w', encoding='utf-8') as f:
        line = '\n'.join(list(sorted(inserts)))
        f.write(line)


def main():
    articlePath = 'adyghePolitics.htm'
    unparsedPath = 'adyghe-unparsed-words.txt'
    articleWords = retrieveArticleWords(articlePath)
    unparsedWords = retrieveUnparsedWords(unparsedPath)
    # задание на 5
    intersectingWords(articleWords, unparsedWords)
    # задание на 8
    wannabeRusNouns = detectRusNouns(unparsedPath)
    # задание на 10
    makeInserts(wannabeRusNouns, 'mystemRes.txt')


if __name__== '__main__':
    main()