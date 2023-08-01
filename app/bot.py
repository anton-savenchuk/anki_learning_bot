import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)

from _messages import messages
from anki_connect import (
    add_note,
    create_deck,
    create_model,
    get_deck_names,
    get_model_names,
)
import config
from main import (
    check_admin_user,
    check_keyword,
    get_card_data,
    get_keyword_data,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages.get("start")
        if check_admin_user(update.effective_user.id)
        else messages.get("private_bot"),
        parse_mode="html",
    )


async def get_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_admin_user(update.effective_user.id):
        flag, fail_message = check_keyword(update.message.text)

        if flag:
            deck_name = "English"
            model_name = "CARDS"
            keyword_data = get_keyword_data(update.message.text)

            with open(keyword_data.get("sound"), "rb") as sound:
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=sound,
                    caption=f'Англ.: <b>{keyword_data.get("keyword")}</b>\n'
                    f'Рус.: <b>{", ".join(keyword_data.get("translation"))}</b>',
                    parse_mode="html",
                )

            if deck_name not in get_deck_names().get("result"):
                create_deck(deck_name)

            if model_name not in get_model_names().get("result"):
                create_model(model_name)

            card_data = get_card_data(keyword_data)
            add_note(deck=deck_name, model=model_name, note=card_data)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=fail_message,
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
    user_text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        get_user_text,
    )

    application.add_handler(start_handler)
    application.add_handler(user_text_handler)

    application.run_polling()
