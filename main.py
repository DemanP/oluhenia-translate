# import logging, os
# from telegram import __version__ as TG_VER

# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0) # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#     f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#     f"{TG_VER} version of this example, "
#     f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
# from telegram import ForceReply, Update
# from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# # Enable logging
# logging.basicConfig(
# format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)


# # Define a few command handlers. These usually take the two arguments update and
# # context.
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /start is issued."""
#     user = update.effective_user
#     await update.message.reply_html(
#     f"Hau {user.mention_html()}!\nНапиши мені речення на українській і я його перекладу на олутонк(або навпаки, з олутонку на українську)",
#     # reply_markup=ForceReply(selective=True),
#     )


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Help!")

# from translate import *

# async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     text = update.message.text
#     result = translate(text)
#     await update.message.reply_text(result)

# TOKEN = "6072135388:AAE2YOduxp_PVixfwzRdCeBvFW1R7dLmJ0c"
# PORT = int(os.environ.get('PORT', '8443'))

# def main() -> None:
#     """Start the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token(TOKEN).build()

#     # on different commands - answer in Telegram
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("help", help_command))

#     # on non command i.e message - echo the message on Telegram
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

#     # Run the bot until the user presses Ctrl-C
#     while 1:
#         try:
#             application.run_polling()
#         except: pass
    
    
#     # application.bot.set_webhook("https://oluhenia-translate.onrender.com/"+TOKEN)
    
#     # application.bot.setWebhook("https://oluhenia-translate.onrender.com/"+TOKEN)
    
#     # application.updater.start_webhook(listen="0.0.0.0",
#     #     port=PORT,
#     #     url_path=TOKEN)
#     # application.updater.bot.setWebhook("https://oluhenia-translate.onrender.com/"+TOKEN)
#     # application.updater.idle()
#     # application.bot.idle()


# if __name__ == "__main__":
#     main()



import logging
import time
from translate import *

import flask

import telebot

API_TOKEN = '6072135388:AAE2YOduxp_PVixfwzRdCeBvFW1R7dLmJ0c'

WEBHOOK_HOST = 'oluhenia-translate.onrender.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, f"Hau {message.from_user.first_name} {message.from_user.last_name}!\nНапиши мені речення на українській і я його перекладу на олутонк(або навпаки, з олутонку на українську)")


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    result = translate(message.text)
    bot.reply_to(message, result)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                # certificate=open(WEBHOOK_SSL_CERT, 'r')
)

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        # ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)