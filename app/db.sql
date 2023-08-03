create table telegram_user (
    id bigint auto_increment primary key,
    anki_user_email text unique,
    anki_user_password text unique
);

create table keyword_data (
    id integer primary key,
    keyword text not null unique,
    translation text,
    examples text,
    sound text,
    sound_url text,
    user_id bigint unique,
    foreign key(user_id) references telegram_user(id),
);
