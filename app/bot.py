import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


from _messages import messages
import config
from main import check_admin_user

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_admin_user(update.effective_user.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.get("start"),
            parse_mode="html",
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.get("private_bot"),
            parse_mode="html",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
