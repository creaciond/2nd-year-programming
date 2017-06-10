from pymorphy2 import MorphAnalyzer


def

def main():
    entering_words = True
    i = 1
    morph_analyzer = MorphAnalyzer()
    print('Чтобы закончить работу с программой, введите пустую строку (т.е. когда вас попросят ввести очередное слово, сразу нажмите Enter).')
    while entering_words:
        word = input('Введите слово %d: ' % i).lower()
        if word == '':
            entering_words = False
        else:
            possible_lemma = morph_analyzer.parse(word)[0]
            tag = str(possible_lemma.tag.POS)
            i += 1


if __name__ == '__main__':
    main()