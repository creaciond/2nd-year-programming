import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

# remove previous webhooks (if any)
bot.remove_webhook()

# new webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)


# /start /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Это бот, который считает длину вашего сообщения.')

# other
@bot.message_handler(func=lambda m: True)
def send_len(message):
    bot.send_message(message.chat.id, 'В вашем сообщении {} слов.'.format(len(message.split(' '))))


# empty main
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# working with webhook
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)