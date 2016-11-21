import re
import os
import html
import json
import codecs
from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)


def cleanLine(line):
    rubbishReg = re.compile('<.*?>')
    additReg = re.compile('\[.*?\]')
    line = rubbishReg.sub('', line)
    line = additReg.sub( '', line)
    line = line.strip(' ')
    return line


# 5 баллов. Скачать отсюда https://yadi.sk/d/e6eos6Czyd4Av архив страниц
# интернет-сайта с тайско-английским словарём. Извлечь с каждой страницы
# пары "тайское слово — английское слово" и поместить их в питоновскую
#структуру данных типа "словарь", где ключом будет тайское слово,
# а значением — английское.
def makeDict():
    thaiDict = {}
    thaiReg = re.compile('<tr><td class=th><a (?:.*?)>(.*?)</a></td><td>(?:.*?)</td><td class=pos>(?:.+?)</td><td>(.*?)</td></tr>')
    for page in os.listdir('./thai_pages'):
        if page.endswith('.html'):
            with open('./thai_pages/' + page, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = html.unescape(line)
                    res = re.findall(thaiReg, line)
                    if res:
                        for each in res:
                            thai = cleanLine(each[0])
                            eng = cleanLine(each[1])
                            if thai and eng and eng != '' and not eng.endswith('\"'):
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


# 10 баллов. Создать на фласке веб-приложение "Англо-тайский словарь", где
# можно было бы в текстовом поле ввести английское слово и получить в
# качестве результата запроса — его перевод на тайский.
@app.route('/')
def search():
    return render_template('index.html')


@app.route('/results')
def results():
    if request.args:
        res = []
        with open('engToThai.json', 'r', encoding='utf-8') as f:
            dictionary = json.loads(f.read())
            searchWord = request.args.get('engWord')
            for item in dictionary:
                if searchWord == item:
                    res.append([item, dictionary[item]])
        return render_template('results.html', query=searchWord, res=res)
                    
        

def main():
    dictionary = makeDict()
    dictToJson(dictionary)
    app.run(debug=True)


if __name__ == '__main__':
    main()
