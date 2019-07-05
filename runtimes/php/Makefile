SHELL := /bin/bash

GREEN   := "\\033[1;32m"
NORMAL  := "\\033[0;39m"
RED     := "\\033[1;31m"
PINK    := "\\033[1;35m"
BLUE    := "\\033[1;34m"
WHITE   := "\\033[0;02m"
YELLOW  := "\\033[1;33m"
CYAN    := "\\033[1;36m"


define php_task
	mkdir files
	python3 ../../bin/docker-template.py --template=$(2).dt --version=$(1)
	mkdir dockerfiles
	mv Dockerfile ./dockerfiles/$(1).d
	mv $(2) ./dockerfiles/$(2).bats
	docker build -f ./dockerfiles/$(1).d -t continuous-php:$(1) .
	cat ../../bin/batsimage.d >> ./dockerfiles/$(1).d
	docker build -f ./dockerfiles/$(1).d -t bats_test .
	docker run -it -v ${PWD}/dockerfiles/$(2).bats:/test.bats bats_test \
|| echo "Bats tests failed"
	docker container prune -f && docker rmi bats_test -f
	rm -rf files dockerfiles
endef


generic:
	$(call php_task,None,generic)
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
	$(call php_task,5.6.4-fpm,phpv1)
.PHONY: php564

php7022:
	$(call php_task,7.0.22-fpm,phpv1)
.PHONY: php7022

php704:
	$(call php_task,7.0.4-fpm,phpv1)
.PHONY: php704

php710:
	$(call php_task,7.1.0-fpm,phpv1)
.PHONY: php710

php7112:
	$(call php_task,7.1.12-fpm,phpv1)
.PHONY: php7112

php720:
	$(call php_task,7.2-fpm,phpv2)
.PHONY: php720

php723:
	$(call php_task,7.2.3-fpm,phpv2)
.PHONY: php723
