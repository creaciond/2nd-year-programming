# -*- coding: utf-8 -*-
import telebot
import conf
import flask

'''
    BOT
'''
# CREATING A BOT
bot = telebot.TeleBot(conf.TOKEN, threaded=False)
app = flask.Flask(__name__)


# WEBHOOKS
# webhook URLs and tokens — in conf.py
WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)


# send_welcome() function for /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет! Этот бот умеет вычислять семантическую близость двух слов и строить граф, где отображается близость этих слов. \n" +
                    "Для того, чтобы получить граф, введите больше одного слова, разделённых пробелом \(например, \"кот кошка играть\"\).")


'''
    FLASK
'''
# empty main for check
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# webhook handling
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
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
    bot.polling(none_stop=True)