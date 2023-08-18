from telegram import Update
from telegram.ext import ContextTypes

from app.anki_connect import get_sync, load_profile
from app.messages import messages


async def get_anki_sync(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_profile("User 1")
    get_sync()  # TODO exceptions

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.get("sync_success"),
        parse_mode="html",
    )
