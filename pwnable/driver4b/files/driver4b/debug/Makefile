debug:
	mkdir -p rootfs
	cd rootfs; cpio -idv <../rootfs.cpio 2>/dev/null
	gcc example.c -o rootfs/example
	cd rootfs; find . -print0 | cpio -o --null --format=newc --owner=root >../rootfs.cpio
	./debug.sh
