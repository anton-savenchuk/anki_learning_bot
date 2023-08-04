create table telegram_user (
    telegram_id bigint primary key,
    anki_user_email text unique,
    anki_user_password text unique
);

create table keyword_data (
    id integer primary key,
    user_id bigint,
    keyword text not null unique,
    translation text,
    examples text,
    examples_translation text,
    sound text,
    sound_url text,
    foreign key(user_id) references bot_user(telegram_id)
);
