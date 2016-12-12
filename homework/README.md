# Домашние работы
(for English version please see below)

## Газетный корпус


__Задание:__ краулером обойти страницы сайта газеты, выгрузить оттуда статьи, записать их (в папке plain), после чего тексты морфологически обработать через [mystem](https://tech.yandex.ru/mystem/ "Сайт и документация на сайте Яндекса") в двух вариантах — xml (папка `mystem-xml`) и txt (папка `mystem-plain`). Вся информация об обработанных статьях — в таблице `metadata.csv` в корневой папке.

Газета — ["Полярная звезда"](http://polkrug.ru/), г. Салехард, Ямало-Ненецкий автономный округ.

Сама домашняя работа — в подпапке **newspaper-corpus**:
+ `metadata.csv` — таблица с информацией об обработанных статьях
+ `plain` — тексты статей, рассортированные по годам, внутри — по месяцам
+ `mystem-xml` — размеченное mystem в формате xml
+ `mystem-plain` — размеченное mystem в формате plain text

Всё, что просто лежит здесь, в папке homework — промежуточный код и тестовые файлы.

## Сайт-анкета на Flask

__Задание:__ написать сайт-анкету с использованием Flask, например, для полевого или социолингвистического исследования. После того, как пользователь заполнил анкету, он должен мочь: посмотреть *статистику* на специальной вкладке, *искать* среди уже заполненных анкет на отдельной вкладке (при этом полей для поиска должно быть больше двух), посмотреть *JSON* уже заполненных анкет.

Результаты должны *сохраняться* в текстовый файл.

Работа находится в папке  __flask-questionnaire__:
+ `templates` — папка с шаблонами html-страниц,
+ `site-code.py` — непосредственно код, запускающий сервер и обрабатывающий все запросы,
+ `data.txt` — все записанные анкеты.

---

# In English

## Newspaper corpus

__Task:__ creating a corpus from a regional newspaper. The code crawls newspaper's webpage, gets article source code, parses it, gets information and saves it. Later on, morphological parsing is being processed via [mystem](https://tech.yandex.ru/mystem/ "Mystem site & documentation, in Russian").

Newspaper: ["Polyarnaya zvezda" (Polar Star)](http://polkrug.ru/), regional newspaper of Yamalo-Nenets Autonomus Okrug, based in Salekhard.

Code itself, output (see the link to Google Drive), etc — in **newspaper-corpus** folder, the rest is WIP. It contains:
+ `metadata.csv` — table with information about the articles parsed
+ `plain` — articles, plain text, sorted via year and month when they were written
+ `mystem-xml` — morphologically annotated articles (after using mystem), xml format
+ `mystem-plain` — morphologically annotated articles (after using mystem), plain text format

## Flask Questionnaire

__Task:__ create a simple website with Flask, for instance, for a field linguistic survey or a sociolinguistic research. After filling in the form the user should be able to: explore *statistics* on a special tab, *search* throughout the data from previous forms (with at least two various search fields), take a look at previous forms' *JSON*-formatted data.

Results *should be saved* in a .txt file.

Code is stored at  __flask-questionnaire__ folder:
+ `templates` — html templates for the website,
+ `site-code.py` — code which runs the server and parses everything,
+ `data.txt` — all the forms filled.
