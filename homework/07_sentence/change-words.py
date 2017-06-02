from pymorphy2 import MorphAnalyzer
import random


def get_popular_words(morph_analyzer):
    lemmas = {}
    with open('./1grams-3.txt', 'r', encoding='utf-8') as f:
        words = [line.split('\t')[1].strip('\n').lower() for line in f.readlines()[:100000]]
    for word in words:
        unchangeable = str(morph_analyzer.parse(word)[0].tag).split(' ')[0]
        lemma = str(morph_analyzer.parse(word)[0].normal_form)
        if unchangeable in set(lemmas.keys()):
            lemmas[unchangeable].append(lemma)
        else:
            ar = []
            ar.append(lemma)
            lemmas[unchangeable] = ar
    return lemmas


def similar_word(words, characteristics, morph_analyzer):
    word = morph_analyzer.parse(random.choice(words[characteristics]))[0].normal_form
    return word


def work_with_words(word, morph_analyzer, popular_words):
    characteristics = str(morph_analyzer.parse(word)[0].tag).split(' ')
    '''
        characteristics[0] — unchangeable
        characteristics[1] — changeable
    '''
    new_word = similar_word(popular_words, characteristics[0], morph_analyzer)
    if len(characteristics) != 1:
        params = set(characteristics[1].split(','))
        new_word_inflected = str(morph_analyzer.parse(new_word)[0].inflect(params).word)
    else:
        new_word_inflected = new_word
    return new_word_inflected


def main():
    morph_analyzer = MorphAnalyzer()
    popular_words = get_popular_words(morph_analyzer)
    enteringWords = True
    marks = '.,?!:;\"\'…'
    i = 1
    print('Пустая строчка — выход из программы.')
    while enteringWords:
        sent = input('Введите предложение %d: ' % i).lower()
        if sent:
            try:
                j = 0
                sentence = sent.split(' ')
                new_sent = []
                for j in range(len(sentence)):
                    new_word = work_with_words(sentence[j], morph_analyzer, popular_words)
                    # first word
                    if j == 0:
                        new_word = new_word.capitalize()
                    # marks
                    for mark in marks:
                        if sentence[j].endswith(mark):
                            new_word += mark
                        else:
                            if sentence[j].startswith(mark):
                                new_word = mark + new_word
                    new_sent.append(new_word)
                print(' '.join(new_sent))
            except:
                print('Что-то не получилось. Давайте другое!')
            i += 1
        else:
            enteringWords = False



if __name__ == '__main__':
    main()