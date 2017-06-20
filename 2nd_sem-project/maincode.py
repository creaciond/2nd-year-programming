# -*- coding: utf-8 -*-
# bot
import telebot
import flask
import os
# code itself
import requests
import networkx as nx
import matplotlib.pyplot as plt

'''
    BOT
'''
# creating a bot
TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN, threaded=False)


'''
    WEBHOOKS
'''
bot.remove_webhook()
bot.set_webhook(url='https://rusvectoresgraph.herokuapp.com/bot')
WEBHOOK_URL_PATH = 'https://rusvectoresgraph.herokuapp.com/bot'


'''
    FLASK
'''
app = flask.Flask(__name__)

'''
    WORK WITH INPUT
'''
def check_message(words):
    alphabet = set(list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя '))
    words = [str(word).strip('.,?!\(\)\[\]\'\"\\').lower() for word in words]
    error_code = 0
    # check for number of words
    if len(words) <= 2:
        error_code = 1
    # check for characters
    i = 0
    while i <= len(words):
        if words[i] not in alphabet:
            error_code = 2
            break
        else:
            i += 1
    # if everything's good so far, no error
    return error_code, words


# gives semantic closeness between pairs of words
def get_closeness(words):
    # semantic_dict = {w1: [distance to w2, distance to w3, etc]}
    semantic_dict = {word: [] for word in words}
    # LINK:
    # http://rusvectores.org/ruscorpora/WORD1__WORD2/api/similarity/
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            link = 'http://rusvectores.org/ruscorpora/%s__%s/api/similarity/' % (words[i], words[j])
            try:
                response = requests.get(link)
                # distance
                dist = float(str(response.text).split()[0])
                # append distance to the referring array in dictionary
                semantic_dict[words[i]].append(dist)
                semantic_dict[words[j]].append(dist)
            except:
                # todo later: send a message that no closeness was found for the pair
                response = {}
    return semantic_dict


def print_error_input(message):
    error_code, words = check_message(message)
    '''
        0 - ok
        1 - length of input
        2 - not in Russian
    '''
    if error_code == 1:
        bot.send_message(message.chat.id, "Кажется, вы ввели два слова или меньше. " +
                         "Наберите /help, чтобы посмотреть пример ввода, и попробуйте ещё раз!")
    elif error_code == 2:
        bot.send_message(message.chat.id, "Кажется, в вашей строке есть символы на латинице. "
                         + "Бот умеет работать только с кириллицей. "
                         + "Не расстраивайтесь, наберите /help, чтобы посмотреть пример ввода, и попробуйте ещё раз!")
    else:
        bot.send_message(message.chat.id, "Всё хорошо, начинаю работать!")
    return error_code, words


def do_graph(semantic_dict):
    distances = []
    gr = nx.Graph()
    # dictionary parsing
    words = list(semantic_dict.keys())
    for word in words:
        i = 0
        values = semantic_dict[word]
        while i < len(values):
            if words[i] == word:
                # this thing is kind of useless, but still
                buf = 1
            else:
                gr.add_edge(word, words[i], weight=values[i])
                word_distance = (word, words[i], values[i])
                distances.append(word_distance)
            i += 1
    # edge thickness
    edges = [d['weight'] for (u, v, d) in gr.edges(data=True)]
    # drawing the graph
    pos = nx.spring_layout(gr)
    nx.draw_networkx_nodes(gr, pos, node_color='gray', node_size=100)
    nx.draw_networkx_edges(gr, pos, edge_color='black', width=edges)
    nx.draw_networkx_labels(gr, pos, font_size=10, font_family='Arial')
    plt.axis('off')
    return plt, distances


'''
    BOT MESSAGES
'''
# send_welcome() function for /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Этот бот умеет вычислять семантическую близость двух слов и"
                     + " строить граф, где отображается близость этих слов. \n"
                     + "Для того, чтобы получить граф, введите команду /get_graph и слова через пробел "
                     + "(например, \"/get_graph кот кошка играть\"). "
                     + "Оптимальное количество — от 7 до 20 слов. \n"
                     + "Чтобы увидеть весь список комманд, наберите /commands.")


# /about
@bot.message_handler(commands='/about')
def tell_about_yourself(message):
    bot.send_message(message.chat.id, "Я бот, который может вычислять семантическую близость двух слов! "
                     + "Меня сделала Даша Максимова, ей можно написать: @zghvebi "
                     + "или на почту: daria.maximova.m@gmail.com")


# /commands
@bot.message_handler(commands='/commands')
def tell_commands(message):
    bot.send_message(message.chat.id, "Вот список комманд: \n"
                     + "/help — выводит подсказку про бота и пример ввода,\n"
                     + "/about — про бота и его создателя,\n"
                     + "/commands — список команд для бота (вы только что использовали это команду),\n"
                     + "/get_graph — получение графа для введённых слов. Слова нужно вводить через пробел после команды,\n"
                     + "/end — закончить общение с ботом. Чтобы начать его снова, введите /start.")


# messages with words
@bot.message_handler(commands='/get_graph')
def do_stuff(message):
    input = message.strip()[1:]
    # check input
    error_code, words = print_error_input(input)
    if error_code == 0:
        #! do semantic closeness
        sem_dict = get_closeness(words)
        # bot.send_message(message.chat.id, sem_dict)
        #! draw graphs
        plot, distances = do_graph(sem_dict)
        dist_to_show = []
        for distance in distances:
            dist_to_show.append('%s — %s: %f' % (distance[0], distance[1], distance[2]))
        bot.send_message(message.chat.id, '\n'.join(dist_to_show), reply_to_message_id=message.message,id)
        bot.send_photo(message.chat.id, plot, reply_to_message_id=message.message_id)

'''
    FLASK
'''
# empty main for check
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# webhook handling
@app.route("/bot", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


'''
    MAIN
'''
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)