all: dist

image: Dockerfile
	docker image build -t pwn_builder:22.04 .

build: src.c Makefile
	docker run -it --rm -v $(shell pwd):/build pwn_builder:22.04

chall: src.c Makefile
	gcc src.c -o chall -fcf-protection=none -Wall -Wextra

clean:
	rm -f chall ../files/chall ../solver/chall
	docker container rm undef_uaf_chall
	docker image rm undef_uaf_undef_uaf

dist: build
	cp chall ../files/
	cp src.c ../files/
	cp chall ../solver/

serve: dist
	docker-compose -f ../docker-compose.yml up --build
