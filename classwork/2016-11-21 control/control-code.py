
# 10 баллов. Создать на фласке веб-приложение "Англо-тайский словарь", где
# можно было бы в текстовом поле ввести английское слово и получить в
# качестве результата запроса — его перевод на тайский.
import re
import os
import json
import codecs


# 5 баллов. Скачать отсюда https://yadi.sk/d/e6eos6Czyd4Av архив страниц
# интернет-сайта с тайско-английским словарём. Извлечь с каждой страницы
# пары "тайское слово — английское слово" и поместить их в питоновскую
#структуру данных типа "словарь", где ключом будет тайское слово,
# а значением — английское.
def makeDict():
    thaiDict = {}
    thaiReg = re.compile('<tr><td class=th><a (?:.*?)>(.*?)</a></td><td>(?:.*?)</td><td class=pos>(?:.*?)</td><td>(.*?)</td></tr>')
    rubbishReg = re.compile('<.*?>')
    additReg = re.compile('\[.*?\]')
    for page in os.listdir('./thai_pages'):
        if page.endswith('.html'):
            with open('./thai_pages/' + page, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = re.sub('&#34;', '\"', line)
                    res = re.findall(thaiReg, line)
                    if res:
                        for each in res:
                            thai = rubbishReg.sub('', each[0])
                            thai = additReg.sub( '', thai)
                            eng = rubbishReg.sub( '', each[1])
                            eng = additReg.sub( '', eng)
                            if eng != '' and not eng.endswith('\"'):
                                thaiDict[thai] = eng
            print(page)
    return thaiDict


# 8 баллов. Использовать структуру данных из предыдущего задания, записать
# её в файл формата json на диск, а также создать ещё одну структуру данных,
# где будет наоборот: английское слово ключ, а значение — массив тайских.
# Её тоже записать на диск в формате json.
def dictToJson(pythonDict):
    thaiToEng = json.dumps(pythonDict)
    with codecs.open('thaiToEng.json', 'w', encoding='utf-8') as out:  
        out.write(thaiToEng)
    invertedDict = {eng:thai for thai, eng in pythonDict.items()}
    engToThai = json.dumps(invertedDict)
    with codecs.open('engToThai.json', 'w', encoding='utf-8') as out:  
        out.write(engToThai)


def main():
    dictionary = makeDict()
    dictToJson(dictionary)


if __name__ == '__main__':
    main()
