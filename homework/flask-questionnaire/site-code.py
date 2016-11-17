import os.path
from urllib.parse import quote, unquote
from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)


# это очень плохо, мне очень стыдно, но пока что версия без глобальных переменных не выходит :(
totalCount = 0
movedCount = 0
totalAge = 0
avAge = 0
regionCount = 0
regions = {} 
diminutives = {"Uliana":[], "Oleg":[], "Vasilisa":[], "Georgij":[], "Alyona":[], 
"Nikita":[], "Kristina":[], "Lev":[], "Alisa":[], "Anna":[], "Alexander":[], 
"Larisa":[], "Ekaterina":[], "Regina":[], "Semyon":[], "Polina":[], "Aleksej":[], 
"Alina":[], "Mihail":[], "Anastasia":[]}


@app.route('/')
def index():
	if request.args:
		f = open('data.txt', 'a', encoding='utf-8')
		f.write('%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s<br /></tab1>' % (int(request.args.get('age')), request.args.get('region_born'), request.args.get('region_now'), request.args.get('Uliana'), request.args.get('Oleg'), request.args.get('Vasilisa'), request.args.get('Georgij'), request.args.get('Alyona'), request.args.get('Nikita'), request.args.get('Kristina'), request.args.get('Lev'), request.args.get('Alisa'), request.args.get('Anna'), request.args.get('Alexander'), request.args.get('Larisa'), request.args.get('Ekaterina'), request.args.get('Regina'), request.args.get('Semyon'), request.args.get('Polina'), request.args.get('Aleksej'), request.args.get('Alina'), request.args.get('Mihail'), request.args.get('Anastasia')))
		f.close()
	return render_template('index.html')


@app.route('/getjson')
def getjson():
	with open('data.txt','r', encoding='utf-8') as f:
		jsonAr = []
		for line in f:
			info = line.split(',')
			jsonLine = '<tab1>age: ' + str(info[0]) + ',<br /></tab1>' + '<tab1>region_born: \"' + info[1] + '\",<br /></tab1>' + '<tab1>region_now: \"' + info[2] + '\",<br /></tab1>' + '<tab1>Uliana: \"' + info[3] + '\",<br /></tab1>' + '<tab1>Oleg: \"' + info[4] + '\",<br /></tab1>' + '<tab1>Vasilisa: \"' + info[5] + '\",<br /></tab1>' + '<tab1>Georgij: \"' + info[6] + '\",<br /></tab1>' + '<tab1>Alyona: \"' + info[7] + '\",<br /></tab1>' + '<tab1>Nikita: \"' + info[8] + '\",<br /></tab1>' + '<tab1>Kristina: \"' + info[9] + '\",<br /></tab1>' + '<tab1>Lev: \"' + info[10] + '\",<br /></tab1>' + '<tab1>Alisa: \"' + info[11] + '\",<br /></tab1>' + '<tab1>Anna: \"' + info[12] + '\",<br /></tab1>' + '<tab1>Alexander: \"' + info[13] + '\",<br /></tab1>' + '<tab1>Larisa: \"' + info[14] + '\",<br /></tab1>' + '<tab1>Ekaterina: \"' + info[15] + '\",<br /></tab1>' + '<tab1>Regina: \"' + info[16] + '\",<br /></tab1>' + '<tab1>Semyon: \"' + info[17] + '\",<br /></tab1>' + '<tab1>Polina: \"' + info[18] + '\",<br /></tab1>' + '<tab1>Aleksej: \"' + info[19] + '\",<br /></tab1>' + '<tab1>Alina: \"' + info[20] + '\",<br /></tab1>' + '<tab1>Mihail: \"' + info[21] + '\",<br /></tab1>' + '<tab1>Anastasia: \"' + info[22] + '\"<br /></tab1>'
			jsonAr.append(jsonLine)
	return render_template('json.html', jsonar=jsonAr)


@app.route('/search')
def search():
	return render_template('search.html')
	# сюда надо прикрутить поиск


@app.route('/statistics')
def stats():
	data = []
	# сменили место жительства
	movedCount = 0
	# для среднего возраста
	totalAge = 0
	# сами регионы
	regions = {} 
	# словарь с вариантами
	diminutives = {'Uliana':[], 'Oleg':[], 'Vasilisa':[], 'Georgij':[], 'Alyona':[], 'Nikita':[], 'Kristina':[], 'Lev':[], 'Alisa':[], 'Anna':[], 'Alexander':[], 'Larisa':[], 'Ekaterina':[], 'Regina':[], 'Semyon':[], 'Polina':[], 'Aleksej':[], 'Alina':[], 'Mihail':[], 'Anastasia':[]}
	dimNames = ['Uliana', 'Oleg', 'Vasilisa', 'Georgij', 'Alyona', 'Nikita', 'Kristina', 'Lev', 'Alisa', 'Anna', 'Alexander', 'Larisa', 'Ekaterina', 'Regina', 'Semyon', 'Polina', 'Aleksej', 'Alina', 'Mihail', 'Anastasia']
	namesTransl = {'Uliana':'Ульяна', 'Oleg':'Олег', 'Vasilisa':'Василиса', 'Georgij':'Георгий', 'Alyona':'Алёна', 'Nikita':'Никита', 'Kristina':'Кристина', 'Lev':'Лев', 'Alisa':'Алиса', 'Anna':'Анна', 'Alexander':'Александр', 'Larisa':'Лариса', 'Ekaterina':'Екатерина', 'Regina':'Регина', 'Semyon':'Семён', 'Polina':'Полина', 'Aleksej':'Алексей', 'Alina':'Алина', 'Mihail':'Михаил', 'Anastasia':'Анастасия'}
	with open('data.txt','r', encoding='utf-8') as f:
		for line in f:
			lineData = line.split(',')
			totalAge += int(lineData[0])
			# для тех, кто переехал
			if lineData[2] != '':
				movedCount += 1 
				if lineData[2] not in regions:
					regions[lineData[2]] = 1
				else:
					regions[lineData[2]] += 1
			# для тех, кто не переезжал 
			else:
				if lineData[1] not in regions:
					regions[lineData[1]] = 1
				else:
					regions[lineData[1]] += 1 
			# записываем сокращения в словарь
			for i in range(3, 23):
				index = dimNames[i-3]
				if lineData[i] not in diminutives[index]:
					diminutives[index].append(lineData[i])
			# на всякий случай закидываем в общий массив
			data.append(lineData)
	# всего заполнили
	totalCount = len(data)
	# средний возраст
	avAge = totalAge/totalCount
	# самый популярные регионы + редкие
	mostRegAr = []
	rareAr = []
	avReg = totalCount/len(regions)
	for region in sorted(regions):
		if regions[region] == 1:
			rareAr.append(region)
		if regions[region] >= avReg:
			mostRegAr.append(region)
	mostReg = ', '.join(mostRegAr)
	rareReg = ', '.join(rareAr) 
	# полный список
	regionsList = ', '.join(regions.keys())
	# процент заполнивших регионов
	regionsPercent = round(len(regions)/85, 2)
	# имена с наибольшей вариативностью
	mostVariants = '(здесь будут какие-то имена [помогите придумать, пжлст!])'
	# в среднем вариантов на имя
	varCount = 0
	sameNamesAr = []
	mostVarsAr = []
	for name in diminutives:
		if len(diminutives[name]) >= 2:
			mostVarsAr.append(name)
		if len(diminutives[name]) == 1:
			sameNamesAr.append(namesTransl[name])
		varCount += len(diminutives[name])
	avVariants = round(varCount/20, 2)
	return render_template('stats.html', totalCount=totalCount,
                               movedCount=movedCount,
                               avAge=avAge,
                               regionCount=regionCount,
                               mostRegions=mostReg,
                               rareRegions=rareReg,
                               regionsList=regionsList,
                               regionsPercent=regionsPercent,
                               mostVariants=', '.join(mostVarsAr),
                               avVariants=avVariants,
                               sameNames=', '.join(sameNamesAr))


if __name__ == '__main__':
	app.run(debug=True)
