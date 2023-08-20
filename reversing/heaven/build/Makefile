.PHONY: build
build: main.c encrypt.s
	gcc -fno-stack-protector -fno-pie -O3 -c -o main.o main.c
	as -o encrypt.o encrypt.s
	gcc -no-pie -o heaven main.o encrypt.o
