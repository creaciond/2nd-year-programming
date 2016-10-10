## Домашние работы

### Газетный корпус
(for English version please see below)
*Задание:* краулером обойти страницы сайта газеты, выгрузить оттуда статьи, записать их (в папке plain), после чего тексты морфологически обработать через [mystem](https://tech.yandex.ru/mystem/ "Сайт и документация на сайте Яндекса") в двух вариантах — xml (папка `mystem-xml`) и txt (папка `mystem-plain`). Вся информация об обработанных статьях — в таблице `metadata.csv` в корневой папке.
Газета — "Полярная звезда", г. Салехард, Ямало-Ненецкий автономный округ.
Адрес: http://polkrug.ru/
Сама домашняя работа — в подпапке **newspaper-corpus**:
+ `metadata.csv` — таблица с информацией об обработанных статьях
+ `plain` — тексты статей, рассортированные по годам, внутри — по месяцам
+ `mystem-xml` — размеченное mystem в формате xml
+ `mystem-plain` — размеченное mystem в формате plain text
Всё, что просто лежит здесь, в папке homework — промежуточный код и тестовые файлы.

#### In English: newspaper corpus
*Task:* creating a corpus from a regional newspaper. The code get article source code, parses it, gets information and saves it. Later on, morphological parsing is being processed via [mystem](https://tech.yandex.ru/mystem/ "Mystem site & documentation, in Russian").
Newspaper: "Polyarnaya zvezda" (Polar Star), regional newspaper of Yamalo-Nenets Autonomus Okrug, based in Salekhard. 
Address: http://polkrug.ru/
Code itself, output (see the link to Google Drive), etc — in **newspaper-corpus** folder, the rest is WIP. It contains:
+ `metadata.csv` — table with information about the articles parsed
+ `plain` — articles, plain text, sorted via year and month when they were written
+ `mystem-xml` — morphologically annotated articles (after using mystem), xml format
+ `mystem-plain` — morphologically annotated articles (after using mystem), plain text format