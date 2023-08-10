from telegram import Update
from telegram.ext import ContextTypes

from app import db
from app.__main__ import (
    check_admin_user,
    check_keyword,
    get_card_data,
    get_keyword_data,
)
from app.anki_connect import (
    add_note,
    create_deck,
    create_model,
    get_deck_names,
    get_model_names,
)
from app.messages import messages


async def get_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_user = update.effective_user.id

    if check_admin_user(bot_user):
        flag, fail_message = check_keyword(update.message.text)

        if flag:
            keyword = update.message.text.lower()

            if db.check_keyword_exists(keyword):
                keyword_data = db.get_keyword_data(keyword, bot_user)
                with open(f'./{keyword_data.get("sound")}', "rb") as sound:
                    await context.bot.send_audio(
                        chat_id=update.effective_chat.id,
                        audio=sound,
                        caption=f'Англ.: <b>{keyword_data.get("keyword")}</b>\n'
                        f'Рус.: <b>{", ".join(keyword_data.get("translation"))}</b>',
                        parse_mode="html",
                    )
            else:
                keyword_data = get_keyword_data(keyword)

                with open(f'./{keyword_data.get("sound")}', "rb") as sound:
                    await context.bot.send_audio(
                        chat_id=update.effective_chat.id,
                        audio=sound,
                        caption=f'Англ.: <b>{keyword_data.get("keyword")}</b>\n'
                        f'Рус.: <b>{", ".join(keyword_data.get("translation"))}</b>',
                        parse_mode="html",
                    )

                deck_name = "English"
                if deck_name not in get_deck_names().get("result"):
                    create_deck(deck_name)

                model_name = "CARDS"
                if model_name not in get_model_names().get("result"):
                    create_model(model_name)

                db.insert_keyword_data(keyword_data, bot_user)
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
