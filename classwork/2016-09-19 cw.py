import re
import urllib.request
import time
import html


def getpage(pageAddress):
    time.sleep(2)
    page = urllib.request.urlopen(pageAddress)
    text = page.read().decode('ISO-8859-1')
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)  # все комментарии
#    file = open('thread.txt', 'a', encoding='utf-8')
    for line in text:
        line = regTag.sub('', line)
        line = regScript.sub('', line)
        line = regComment.sub('', line)
        line = html.unescape(line)
        print(line)
#        file.write(line)
#    file.close()


def getthread(thrAddress):
    page = urllib.request.urlopen(thrAddress)
    file = open('thread.txt', 'w', encoding='utf-8')
    file.close()        # создали файл, если его не было, если был, то стёрли всё внутри
    text = page.read().decode('ISO-8859-1')
    regLast = re.compile('<span class=\"first_last\"><a (.*)?href=\"((.*)?(page(.*)?))\">', flags=re.U | re.DOTALL)
    lastNum = 0
    for line in text:
        if re.search(regLast, line):
            lastNum = int(regLast.group(4))
            print(lastNum)
            pageAddress = regLast.group(2)
            print(pageAddress)
    if lastNum == 0:
        print('Тред одностраничный')
    else:
        for i in range(1, lastNum+1):
            # "отрезаем" столько символов с конца, сколько цифр в номере последней страница, т.е. саму последнюю страницу
            pageAddress = pageAddress[0:len(pageAddress)-(lastNum // 10)]
            getpage('http://www.forumishqiptar.com/'+pageAddress+str(i))

                                      
if __name__ == '__main__':
    commonUrl = 'http://www.forumishqiptar.com/threads/'
    for i in range(160400, 160425):
        pageUrl = commonUrl + str(i)
        getthread(pageUrl)
