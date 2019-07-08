SHELL := /bin/bash

GREEN   := "\\033[1;32m"
NORMAL  := "\\033[0;39m"
RED     := "\\033[1;31m"
PINK    := "\\033[1;35m"
BLUE    := "\\033[1;34m"
WHITE   := "\\033[0;02m"
YELLOW  := "\\033[1;33m"
CYAN    := "\\033[1;36m"


define node_task
	mkdir files
	python3 ../../bin/docker-template.py --template=$(2).dt
	mkdir dockerfiles
	mv Dockerfile ./dockerfiles/$(1).d
	mv $(2) ./dockerfiles/$(2).bats
	docker build -f ./dockerfiles/$(1).d -t continuous-php:$(1) .
	cat ../../bin/batsimage.d >> ./dockerfiles/$(1).d
	docker build -f ./dockerfiles/$(1).d -t bats_test .
	docker run -it -v ${PWD}/dockerfiles/$(2).bats:/test.bats bats_test \
|| echo "Bats tests failed"
	docker rmi bats_test -f
	rm -rf files dockerfiles
endef

node:
	$(call node_task,node,node)
.PHONY: node
