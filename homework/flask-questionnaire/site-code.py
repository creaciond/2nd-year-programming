from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)


# мне стыдно, но это глобальные переменные
jsonar = []
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


def addDiminutives(form):
	for name in diminutives:
		if form[name] not in diminutives[name]:
			diminutives[name].append(form[name])


@app.route('/')
def index():
	return render_template('index.html')
	if request.args:
		form = request.args
		totalCount += 1
		if form[region_now] != '':
			movedCount = movedCount + 1 
		avAge = (totalAge + int(form[age]))/totalCount
		if form[region_now] != '':
			if form[region_now] not in regions:
				regions[form[region_now]] += 1
			else:
				regions[form[region_born]] = 1
		jsonar.append(form)
		addDiminutives(form)


@app.route('/getjson')
def getjson():
	return render_template('json.html', jsonAr=jsonar)


@app.route('/search')
def search():
	return render_template('search.html')
	

@app.route('/statistics')
def stats():
	mostReg = 'текст'
	# редкие
	rareAr = []
	for region in sorted(regions):
		if regions[region] == 1:
			rareAr += region
	rareReg = ', '.join(rareAr) 
	# полный список
	regionsList = ', '.join(regions.keys())
	# процент заполнивших регионов
	regionsPercent = regionCount/85
	# имена с наибольшей вариативностью
	mostVariants = '(здесь будут какие-то имена [помогите придумать, пжлст!])'
	# в среднем вариантов на имя
	avVariants = 0
	# имена, для которых все дали один и тот же ответ
	sameNames = '(здесь будут какие-то имена [помогите придумать, пжлст!])'
	return render_template('stats.html', totalCount=totalCount,
                               movedCount=movedCount,
                               avAge=avAge,
                               regionCount=regionCount,
                               mostRegions=mostReg,
                               rareRegions=rareReg,
                               regionsList=regionsList,
                               regionsPercent=regionsPercent,
                               mostVariants=mostVariants,
                               avVariants=avVariants,
                               sameNames=sameNames)


if __name__ == '__main__':
	app.run(debug=True)
