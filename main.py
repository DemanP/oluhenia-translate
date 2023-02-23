import logging, os
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0) # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
    f"This example is not compatible with your current PTB version {TG_VER}. To view the "
    f"{TG_VER} version of this example, "
    f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
    f"Hau {user.mention_html()}!\nНапиши мені речення на українській і я його перекладу на олутонк(або навпаки, з олутонку на українську)",
    # reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("He lp!")

from translate import *

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    text = update.message.text
    result = translate(text)
    # result = ""
    # for word in text.split():
    # wordt = word
    # if word.lower() in words:
    # wordt = words[word.lower()]
    # elif word.lower() in translates:
    # wordt = translates[word.lower()]
    # if iscapital(word):
    # wordt = wordt.capitalize()
    # result += " " + wordt
    await update.message.reply_text(result)

TOKEN = "6072135388:AAElf063KT8NkvaVPcXD0-IAHU3b6YK50N0"
PORT = int(os.environ.get('PORT', '8443'))

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    
    application.bot.set_webhook(listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN, url="https://oluhenia-translate.onrender.com")
    # application.bot.idle()


if __name__ == "__main__":
    main()