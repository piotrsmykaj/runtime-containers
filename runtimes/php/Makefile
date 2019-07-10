SHELL := /bin/bash

GREEN   := "\\033[1;32m"
NORMAL  := "\033[0;39m"
RED     := "\033[1;31m"
PINK    := "\\033[1;35m"
BLUE    := "\\033[1;34m"
WHITE   := "\\033[0;02m"
YELLOW  := "\\033[1;33m"
CYAN    := "\\033[1;36m"


define php_task
	make clean
	python3 ../../bin/docker-template.py --template=$(1).xml --base=$(2) --tag=$(3)
endef


generic:
	$(call php_task,generic,debian:jessie,continuousphp:generic)
.PHONY: generic

# Obsolete tags

# php5327:
# 	$(call php_task,5.3.27-fpm,phpv1)
# .PHONY: php5327

# php5421:
# 	$(call php_task,5.4.21-fpm,phpv1)
# .PHONY: php5421

# php5422:
# 	$(call php_task,5.4.22-fpm,phpv1)
# .PHONY: php5422

# php533:
# 	$(call php_task,5.3.3-fpm,phpv1)
# .PHONY: php533

# php5513:
# 	$(call php_task,5.5.13-fpm,phpv1)
# .PHONY: php5513

# php556:
# 	$(call php_task,5.5.6-fpm,phpv1)
# .PHONY: php556

php564:
	$(call php_task,generic,php:5.6.4-fpm,continuousphp:5.6.4-fpm)
.PHONY: php564

php7022:
	$(call php_task,generic,php:7.0.22-fpm,continuousphp:7.0.22-fpm)
.PHONY: php7022

php704:
	$(call php_task,generic,php:7.0.4-fpm,continuousphp:7.0.4-fpm)
.PHONY: php704

php710:
	$(call php_task,generic,php:7.1.0-fpm,continuousphp:7.1.0-fpm)
.PHONY: php710

php7112:
	$(call php_task,generic,php:7.1.12-fpm,continuousphp:7.1.12-fpm)
.PHONY: php7112

php720:
	$(call php_task,generic,php:7.2-fpm,continuousphp:7.2-fpm)
.PHONY: php720

php723:
	$(call php_task,generic,php:7.2.3-fpm,continuousphp:7.2.3-fpm)
.PHONY: php723

clean:
	rm -rf files dockerfiles
.PHONY: clean

clean_image:
	docker rmi $(docker images | grep "continuousphp")
.PHONY: clean_image
