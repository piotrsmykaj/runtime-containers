#!/bin/bash
set -e

if [[ "$PHP_VERSION" < "7.1.40" ]]; then
    apt-get update \
    && apt-get install -y libsodium-dev \
    && apt-get autoremove --purge -y \
    && apt-get autoclean -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*
    pecl install -f libsodium
    docker-php-ext-enable sodium
fi

if [[ "$PHP_VERSION" < "7.4.0" ]]; then
  docker-php-ext-install recode
fi


if [[ "$PHP_VERSION" < "7.1.0" ]]; then
  pecl install xdebug-2.9.0
else
  pecl install xdebug
fi
docker-php-ext-enable xdebug.so