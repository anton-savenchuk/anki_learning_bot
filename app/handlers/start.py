from telegram import Update
from telegram.ext import ContextTypes

from app import db
from app.__main__ import check_admin_user
from app.messages import messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_user = update.effective_user.id

    if check_admin_user(bot_user):
        db.create_bot_user_table()
        db.create_keyword_data_table()

        if not db.check_user_exists(bot_user):
            db.insert_user(bot_user)

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
