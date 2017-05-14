import os
# from sql import *
# from sql.aggregate import *
# from sql.conditionals import *


'''tables in database:
    lemmas — lemmaID, wordform and lemma,
    wordEntries — id, wordform, amark, bmark, isWord, textPosition, lemmaID
'''

# retrieve words
def getWordforms():
    wordforms = []
    insertLineData = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        words = f.read().split()
    return words


# form INSERT lines
def wordformEntry(id, word, amark, bmark, isWord, textPosition, lemmaID, dataAr):
    entry = 'INSERT INTO wordEntries (id, wordform, amark, bmark, isWord, textPosition, lemmaid) VALUES (%d, \"%s\", %d, %d, %d, %d, %d);' % (id, word, amark, bmark, isWord, lemmaID, textPosition)
    dataAr.append(entry)
    textPosition += 1
    return dataAr, textPosition


def lemmaEntry(count, wordform, lemma, data):
    entry = 'INSERT INTO lemmas (id, wordform, lemma) VALUES (%d, \"%s\", \"%s\");' % (count, wordform, lemma)
    if entry not in data:
        data.add(entry)
    return data


# search lemma ID for a wordform
def searchLemma(wordform, lemmaIDs):
    wordform = wordform.lower()
    if wordform in lemmaIDs:
        return lemmaIDs[wordform]
    else:
        return 0


# information for wordforms
# insert lines for wordEntries table
def insertWordforms(words, lemmaIDs):
    insertLineData = []
    posCount = 0
    for word in words:
        # flags for punctuation marks
        amark = 0
        bmark = 0
        wordWithoutMarks = word.strip(' .,?!\"—\(\)\[\]:;')
        if word != wordWithoutMarks and wordWithoutMarks:
            if word[0] != wordWithoutMarks[0]:
                # first symbol is a punсtuation mark; it should be appended before word itself
                amark = 1
                if word[0] == '\'':
                    symbol = 2 * word[0]
                else:
                    symbol = word[0]
                insertLineData, posCount = wordformEntry(posCount, symbol, 0, 0, 0, posCount, searchLemma(wordWithoutMarks, lemmaIDs), insertLineData)
            if word[len(word) - 1] != wordWithoutMarks[len(wordWithoutMarks) - 1]:
                # last symbol is a punctuation mark; it will be appended after word itself
                bmark = 1
        # INSERT for words
        if wordWithoutMarks:
            insertLineData, posCount = wordformEntry(posCount, wordWithoutMarks, amark, bmark, 1, posCount, searchLemma(wordWithoutMarks, lemmaIDs), insertLineData)
            if bmark == 1:
                if word[len(word) - 1] == '\'':
                    symbol = 2 * word[len(word) - 1]
                else:
                    symbol = word[len(word) - 1]
                insertLineData, posCount = wordformEntry(posCount, symbol, 0, 0, 0, posCount, searchLemma(wordWithoutMarks, lemmaIDs), insertLineData)
        # INSERT for punctuation marks
        else:
            insertLineData, posCount = wordformEntry(posCount, word, 0, 0, 0, posCount, searchLemma(wordWithoutMarks, lemmaIDs), insertLineData)
        # save insert commands for wordEntries
        with open('wordEntries.txt', 'w', encoding='utf-8') as f:
            line = '\r\n'.join(insertLineData)
            f.write(line)


def mystemWords(words):
    lowercaseWords = []
    for word in words:
        word = word.lower().strip(' .,?!\"—()')
        if word:
            lowercaseWords.append(word)
    filename = 'lemmasList.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        line = '\n'.join(lowercaseWords)
        f.write(line)
    return filename


def useMystem(wordformsPath):
    mystemPath = '/Users/dariamaximova/Desktop/HSE/Программирование/mystem'
    # paths for source and goal files
    sourcePath = '.' + os.sep + wordformsPath
    goalFileName = 'mystemRes.txt'
    goalPath = '.' + os.sep + goalFileName
    # -cnd == all input to output, each word on new line, context disambiguation
    mystemCommand = mystemPath + ' ' + sourcePath + ' ' + goalPath + ' ' + '-cnd'
    os.system(mystemCommand)
    return goalFileName


def getLemmas(lemmasFile):
    with open(lemmasFile, 'r', encoding='utf-8') as f:
        lemmaEntryData = set()
        wordLemmaPairs = {}
        lemmaCount = 0
        for line in f.readlines():
            # if there's a {, there's a pair wordform{lemma} in the line
            if '{' in line:
                lineItems = line.split('{')
                lemmaEntryData = lemmaEntry(lemmaCount, lineItems[0], lineItems[1].strip('}\n'), lemmaEntryData)
                # dictionary — for lemmaIDs further on
                wordLemmaPairs[lineItems[0]] = lemmaCount
                lemmaCount += 1
    with open('lemmaEntries.txt', 'w', encoding='utf-8') as f:
        line = '\r\n'.join(sorted(list(lemmaEntryData)))
        f.write(line)
    return wordLemmaPairs


def main():
    wordforms = getWordforms()
    # lemmas
    lemmaIDs = getLemmas(useMystem(mystemWords(wordforms)))
    insertWordforms(wordforms, lemmaIDs)



if __name__ == '__main__':
    main()