#!/bin/sh

echo "Updating apt"
apt-get update -y

echo "Installing libraries"
apt-get install -y libpspell-dev librabbitmq-dev libbz2-dev libenchant-dev libwebp-dev libjpeg-dev libpng-dev libz-dev \
    libgmp-dev libc-client-dev libkrb5-dev libicu-dev libldap2-dev libmemcached-dev libpq-dev  \
    librecode-dev libsnmp-dev libxml2-dev libtidy-dev libxslt-dev

echo "Using pecl for some extensions"
pecl install amqp apcu ast memcached mongodb redis xdebug

echo "Using docker-php-ext-configure"
docker-php-ext-configure imap --with-kerberos --with-imap-ssl

echo "Using docker-php-ext-install"
docker-php-ext-install bcmath bz2 calendar dba enchant exif gd gettext gmp imap intl ldap mysqli pcntl pdo_mysql \
    pdo_pgsql pgsql pspell recode shmop snmp soap sockets sysvmsg sysvsem sysvshm tidy xmlrpc xsl zip

echo "Using docker-php-ext-enable"
docker-php-ext-enable amqp.so ast.so apcu.so memcached.so mongodb.so redis.so xdebug.so

echo "Getting oracle instant client"
wget -O ./instantclient-basic.zip \
https://continuousphp-infra.s3-us-west-1.amazonaws.com/oracle/php_runtime/instantclient-basic-linux.x64-19.3.0.0.0dbru.zip
wget -O ./instantclient-sdk.zip \
https://continuousphp-infra.s3-us-west-1.amazonaws.com/oracle/php_runtime/instantclient-sdk-linux.x64-19.3.0.0.0dbru.zip
unzip instantclient-basic.zip && unzip instantclient-sdk.zip
mv instantclient_19_3 /usr/local/instantclient
echo /usr/local/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf
ldconfig
apt-get install -y build-essential libaio1

echo "Installing OCI8"
echo "instantclient,/usr/local/instantclient" | pecl install oci8 && docker-php-ext-enable oci8.so
