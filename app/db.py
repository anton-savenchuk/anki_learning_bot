import sqlite3

from app import config


def create_bot_user_table() -> None:
    sql = """
        CREATE TABLE IF NOT EXISTS bot_user (
            telegram_id bigint primary key,
            anki_user_email text unique,
            anki_user_password text unique
        );
        """

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()

        cursor.execute(sql)

        db.commit()


def create_keyword_data_table() -> None:
    sql = """
        CREATE TABLE IF NOT EXISTS keyword_data (
            id integer primary key,
            user_id bigint unique,
            keyword text not null unique,
            translation text,
            examples text,
            examples_translation text,
            sound text,
            sound_url text,
            foreign key(user_id) references bot_user(telegram_id)
        );
        """

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()

        cursor.execute(sql)

        db.commit()


def check_keyword_exists(keyword: int) -> bool:
    sql = "SELECT keyword FROM keyword_data WHERE keyword=:keyword;"

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute(
            sql,
            {"keyword": keyword},
        )
        keyword_exists = cursor.fetchone()

    return keyword_exists is not None


def insert_keyword_data(keyword_data: dict, user_id: int) -> None:
    sql = """
        INSERT OR IGNORE INTO keyword_data
            (
                keyword,
                translation,
                examples,
                examples_translation,
                sound,
                sound_url,
                user_id
            )
        VALUES (
                :keyword,
                :translation,
                :examples,
                :examples_translation,
                :sound,
                :sound_url,
                :user_id
            )
        """

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute(
            sql,
            {
                "keyword": keyword_data.get("keyword"),
                "translation": ", ".join(keyword_data.get("translation")),
                "examples": " | ".join(keyword_data.get("examples")),
                "examples_translation": " | ".join(
                    keyword_data.get("examples_translation")
                ),
                "sound": keyword_data.get("sound"),
                "sound_url": keyword_data.get("sound_url"),
                "user_id": user_id,
            },
        )

        db.commit()


def check_user_exists(user_id: int) -> bool:
    sql = "SELECT telegram_id FROM bot_user WHERE telegram_id=:user_id;"

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute(
            sql,
            {"user_id": user_id},
        )
        user_exists = cursor.fetchone()

    return user_exists is not None


def insert_user(user_id: int) -> None:
    sql = "INSERT OR IGNORE INTO bot_user (telegram_id) VALUES (:telegram_id);"

    with sqlite3.connect(config.SQLITE_DB_FILE) as db:
        cursor = db.cursor()
        cursor.execute(sql, {"telegram_id": user_id})

        db.commit()


if __name__ == "__main__":
    create_bot_user_table()
    create_keyword_data_table()
