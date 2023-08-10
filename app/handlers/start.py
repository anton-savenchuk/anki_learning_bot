from telegram import Update
from telegram.ext import ContextTypes

from app import db
from app.__main__ import check_admin_user
from app.messages import messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db.create_bot_user_table()
    db.create_keyword_data_table()

    bot_user = update.effective_user.id

    if not db.check_user_exists(bot_user):
        db.insert_user(bot_user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.get("start")
        if check_admin_user(bot_user)
        else messages.get("private_bot"),
        parse_mode="html",
    )
