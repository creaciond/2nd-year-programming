# -*- coding: utf-8 -*-
# bot
import telebot
from telebot import types
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
def check_message(message):
    words_line = message.text.lower()
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    error_code = 0
    # check for number of words
    if len(words_line.split()) <= 3:
        error_code = 1
    # check for characters
    i = 0
    while i <= len(words_line):
        if words_line[i] not in alphabet:
            error_code = 2
            break
        else:
            i += 1
    # if everything's good so far, no error
    return error_code


def print_error(message):
    error_code = check_message(message)
    if error_code == 1:
        bot.send_message(message.chat.id, "Кажется, вы ввели два слова или меньше. " +
                         "Наберите /help, чтобы посмотреть пример ввода, и попробуйте ещё раз!")
    elif error_code == 2:
        bot.send_message(message.chat.id, "Кажется, в вашей строке есть символы на латинице. "
                         + "Бот умеет работать только с кириллицей. "
                         + "Не расстраивайтесь, наберите /help, чтобы посмотреть пример ввода, "
                         + "и попробуйте ещё раз!")
    else:
        bot.send_message(message.chat.id, "Всё хорошо, начинаю работать!")

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


def do_graph(semantic_dict):
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
            i += 1
    # edge thickness
    edges = [d['weight'] for (u, v, d) in gr.edges(data=True)]
    # drawing the graph
    pos = nx.spring_layout(gr)
    nx.draw_networkx_nodes(gr, pos, node_color='gray', node_size=100)
    nx.draw_networkx_edges(gr, pos, edge_color='black', width=edges)
    nx.draw_networkx_labels(gr, pos, font_size=10, font_family='Arial')
    plt.axis('off')
    return plt


def do_distances(semantic_dict):
    distances = []
    words = list(semantic_dict.keys())
    for word in words:
        i = 0
        values = semantic_dict[word]
        while i < len(values):
            if words[i] == word:
                # this thing is kind of useless, but still
                buf = 1
            else:
                word_distance = (word, words[i], values[i])
                distances.append(word_distance)
            i += 1
    message_dist = '\n'.join(distances)
    return message_dist


# main
def assemble(message):
    if message.text != '':
        msg = bot.send_message(message.chat.id, "Введите слова для построения графа (не менее 2),"
            + " разделённые пробелом")
        bot.register_next_step_handler(msg, print_error)
        if check_message(msg) == 0:
            words = [word.strip('.,?!') for word in msg.text.lower().split()]
            # 1. do semantic closeness
            sem_dict = get_closeness(words)
            # 2. do distance
            message_distances = do_distances(sem_dict)
            # 3. draw graphs
            plot = do_graph(sem_dict)
            # 4. show results
            bot.send_message(msg.chat.id, message_distances)
            bot.send_photo(msg.chat.id, plot)


'''
    BOT MESSAGES
'''
# send_welcome() function for /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('/get_graph')
    btn2 = types.KeyboardButton('/help')
    btn3 = types.KeyboardButton('/about')
    btn4 = types.KeyboardButton('/commands')
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Привет! Этот бот умеет вычислять семантическую близость двух слов и"
                     + " строить граф, где отображается близость этих слов. \n"
                     + "Для того, чтобы получить граф, введите команду /get_graph, а затем — слова через пробел "
                     + "(например, \"/get_graph (enter) кот кошка играть\"). "
                     + "Оптимальное количество — от 7 до 20 слов. \n"
                     + "Чтобы увидеть весь список комманд, наберите /commands.", reply_markup=keyboard)


@bot.message_handler(commands=['about'])
def tell_about_yourself(message):
    bot.send_message(message.chat.id, "Я бот, который может вычислять семантическую близость двух слов! "
                     + "Меня сделала Даша Максимова, ей можно написать: @zghvebi "
                     + "или на почту: daria.maximova.m@gmail.com")


@bot.message_handler(commands=['commands'])
def tell_commands(message):
    bot.send_message(message.chat.id, "Вот список комманд: \n"
                     + "/help — выводит подсказку про бота и пример ввода,\n"
                     + "/about — про бота и его создателя,\n"
                     + "/commands — список команд для бота (вы только что использовали это команду),\n"
                     + "/get_graph — получение графа для введённых слов. Слова нужно вводить через "
                     + "пробел.")


@bot.message_handler(commands=['get_graph'])
def get_graph(message):
    bot.register_next_step_handler(message, assemble)

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
