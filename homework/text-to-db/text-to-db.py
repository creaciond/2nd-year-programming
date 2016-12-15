def getWordForms():
    wordForms = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        words = f.read().lower().split()
        for word in words:
            word = word.strip(' .,?!\"—()')
            if word:
                wordForms.append(word)
    return wordForms


def main():
    wordForms = getWords()


if __name__ == '__main__':
    main()