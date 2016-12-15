import os


def getWordforms():
    wordforms = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        words = f.read().lower().split()
        for word in words:
            word = word.strip(' .,?!\"—()')
            if word:
                wordforms.append(word)
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