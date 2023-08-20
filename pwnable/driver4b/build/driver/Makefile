obj-m := ctf4b.o
KBUILD_DIR := /home/ptr/app/buildroot/output/build/linux-6.3.2

all:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) modules

clean:
	$(MAKE) -C $(KBUILD_DIR) M=$(shell pwd) clean
