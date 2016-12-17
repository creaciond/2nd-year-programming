import os


'''tables in database:
    lemmas — lemmaID, wordform and lemma,
    wordEntries — id, wordform, amark, bmark, isWord, textPosition, lemmaID
'''

def makeEntry(word, amark, bmark, isWord, textPosition, dataAr):
    entry = 'INSERT INTO wordEntries (wordform, amark, bmark, isWord, textPosition, lemmaid) VALUES \"%s\", %d, %d, %d, %d, 0' % (word, amark, bmark, isWord, textPosition)
    dataAr.append(entry)
    textPosition += 1
    return dataAr, textPosition


def getWordforms():
    wordforms = []
    insertLineData = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        words = f.read().split()
        posCount = 0
        # insert lines for wordEntries table
        for word in words:
            # flags for punctuation marks
            amark = 0
            bmark = 0
            wordWithoutMarks = word.strip(' .,?!\"—()')
            if word != wordWithoutMarks and wordWithoutMarks:
                if word[0] != wordWithoutMarks[0]:
                    # first symbol is a puntuation mark; it should be appended before word
                    amark = 1
                    insertLineData, posCount = makeEntry(word[0], 0, 0, 0, posCount, insertLineData)
                if word[len(word)-1] != wordWithoutMarks[len(wordWithoutMarks)-1]:
                    # last symbol is a punctuation mark; it will be appended after word
                    bmark = 1
            # INSERT for words
            if wordWithoutMarks:
                wordforms.append(wordWithoutMarks.lower())
                insertLineData, posCount = makeEntry(wordWithoutMarks, amark, bmark, 1, posCount, insertLineData)
                if bmark == 1:
                    insertLineData, posCount = makeEntry(word[len(word)-1], 0, 0, 0, posCount, insertLineData)
            # INSERT for punctuation marks
            else:
                insertLineData, posCount = makeEntry(word, 0, 0, 0, posCount, insertLineData)
    # save insert commands for wordEntries
    with open('wordEntries.txt', 'w', encoding='utf-8') as f:
        line = '\r\n'. join(insertLineData)
        f.write(line)
    # wordforms — lowered words for mystem parsing
    return wordforms


def useMystem(wordformsPath):
    mystemPath = '/Users/dariamaximova/Desktop/HSE/Программирование/mystem'
    # paths for source and goal files
    sourcePath = '.' + os.sep + wordformsPath
    goalPath = '.' + os.sep + 'mystemRes.txt'
    # -cnd == all input to output, each word on new line, context disambiguation
    mystemCommand = mystemPath + ' ' + sourcePath + ' ' + goalPath + ' ' + '-cnd'
    os.system(mystemCommand)



def main():
    wordforms = getWordforms()
    with open('wordforms.txt', 'w', encoding='utf-8') as f:
        line = ' '.join(wordforms)
        f.write(line)
    useMystem('wordforms.txt')


if __name__ == '__main__':
    main()