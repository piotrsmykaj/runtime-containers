SHELL := /bin/bash


generic = $(foreach runtime,$(shell ls runtimes | sed 's/.yml//'),./bin/docker-template --runtime $(runtime) --clean $(1);)

build:
	$(call generic,--verbose --replace build)

test: 
	$(call generic,test)
