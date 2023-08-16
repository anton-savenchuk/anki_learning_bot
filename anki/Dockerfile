ARG APP_NAME=anki
ARG APP_PATH=/opt/$APP_NAME
ARG ANKI_VERSION=2.1.65

FROM ghcr.io/linuxserver/baseimage-kasmvnc:debianbullseye
ARG APP_NAME
ARG APP_PATH
ARG ANKI_VERSION

ENV TITLE=AnkiDesktop

EXPOSE 8765
WORKDIR $APP_PATH
COPY /root /

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        anki \
        mpv \
        wget \
        zstd \
        xdg-utils && \
    dpkg --remove anki && \
    \
    wget https://github.com/ankitects/anki/releases/download/$ANKI_VERSION/anki-$ANKI_VERSION-linux-qt5.tar.zst && \
    tar --use-compress-program=unzstd -xvf anki-$ANKI_VERSION-linux-qt5.tar.zst && \
    cd anki-$ANKI_VERSION-linux-qt5 && ./install.sh && cd .. && \
    \
    rm -rf anki-$ANKI_VERSION-linux-qt5 anki-$ANKI_VERSION-linux-qt5.tar.zst && \
    apt-get clean -y && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /var/cache/apt
