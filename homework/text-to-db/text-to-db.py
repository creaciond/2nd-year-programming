import os


'''tables in database:
    lemmas — lemmaID, wordform and lemma,
    wordEntries — id, wordform, amark, bmark, textPosition, lemmaID
'''


def getWordforms():
    wordforms = []
    insertLineData = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        words = f.read().split()
        posCount = 0
        # insert lines for wordEntries table
        for word in words:
            # flags for marks
            amark = 0
            bmark = 0
            isWord = 0
            wordWithoutMarks = word.strip(' .,?!\"—()')
            if word != wordWithoutMarks and wordWithoutMarks:
                if word[0] != wordWithoutMarks[0]:
                    amark = 1
                if word[len(word)-1] != wordWithoutMarks[len(wordWithoutMarks)-1]:
                    bmark = 1
            # INSERT for words
            if wordWithoutMarks:
                isWord = 1
                wordforms.append(wordWithoutMarks.lower())
                insertLine = 'INSERT INTO wordEntries (wordform, amark, bmark, isWord, textPosition, lemmaid) VALUES \"%s\", %d, %d, %d, %d, 0' % (wordWithoutMarks, amark, bmark, isWord, posCount)
                insertLineData.append(insertLine)
            # INSERT for punctuation marks
            else:
                isWord = 0
                insertLine = 'INSERT INTO wordEntries (wordform, amark, bmark, isWord, textPosition, lemmaid) VALUES \"%s\", %d, %d, %d, %d, 0' % (word, amark, bmark, isWord, posCount)
                insertLineData.append(insertLine)
            posCount += 1
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