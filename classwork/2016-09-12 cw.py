import urllib.request
import re


## Задание из текста семинара
##url = 'https://habrahabr.ru/'                               # адрес страницы, которую мы хотим скачать
##user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'     # хотим притворяться браузером
##
##req = urllib.request.Request('https://habrahabr.ru/', headers={'User-Agent':user_agent})  
### добавили в запрос информацию о том, что мы браузер Мозилла
##
##with urllib.request.urlopen(req) as response:
##    html = response.read().decode('utf-8')
##    regPostTitle = re.compile('<h2 class="post__title">.*?</h2>', flags=re.U | re.DOTALL)
##    titles = regPostTitle.findall(html)
##    new_titles = []
##    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
##    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
##    for t in titles:
##        clean_t = regSpace.sub("", t)
##        clean_t = regTag.sub("", clean_t)
##        new_titles.append(clean_t)
##    for t in new_titles:
##        print(t.replace("&nbsp;&rarr;", " -> "))


## Задание про Яндекс.Погоду
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
# <span class="current-weather__comment">облачно с прояснениями</span>
req = urllib.request.Request('https://yandex.ru/pogoda/moscow/', headers={'User-Agent':user_agent})
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    regWeatherInfo = re.compile('<span class="current-weather__comment">.*?</span>', flags=re.U | re.DOTALL)
    weather_now = regWeatherInfo.findall(html)
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for weather in weather_now:
        weather = regTag.sub('', weather)
        weather = regSpace.sub('', weather)
        print(weather)
# <div class="current-weather__thermometer current-weather__thermometer_type_now">+18 °C</div>
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    regTempInfo = re.compile('<div class="current-weather__thermometer current-weather__thermometer_type_now">.*?</div>', flags=re.U | re.DOTALL)
    temp_now = regTempInfo.findall(html)
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for temp in temp_now:
        temp = regTag.sub('', temp)
        temp = regSpace.sub('', temp)
        print(temp)
# <div class="current-weather__info-row">
#       <span class="current-weather__info-label">Восход: </span>05:55
#       <span class="current-weather__info-label current-weather__info-label_type_sunset">Закат: </span>18:54
# </div>
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    regTimesInfo = re.compile('<div class="current-weather__info-row">.*?</div>', flags=re.U | re.DOTALL)
    times_now = regTimesInfo.findall(html)
    regTag = re.compile('<.*?: </span>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for time in times_now:
        time = regTag.sub('', time)
        time = regSpace.sub('', time)
        if re.search('[0-2][0-9]:[0-5][0-9]', time):
            print(time[0:5], ' ', time[5:10])

#<div class="forecast-brief__item-date">
#	<span class="forecast-brief__item-day-name">вт</span>
#	<span class="forecast-brief__item-day">13</span>
#</div>
#<div class="forecast-brief__item-description t t_c_15">
#	<i class="icon icon_thumb_bkn-d icon_size_30" aria-hidden="true" data-width="30"></i>
#	<div class="forecast-brief__item-comment">малооблачно</div>
#	<div class="forecast-brief__item-temp-day" title="Максимальная температура днём">+15</div>
#</div>
#<div class="forecast-brief__item-temp-night t t_c_7" title="Минимальная температура ночью">+7</div>
