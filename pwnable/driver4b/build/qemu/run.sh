#!/bin/sh
LENGTH=9
STRENGTH=27
challenge=`dd bs=32 count=1 if=/dev/urandom 2>/dev/null | base64 | tr +/ _. | cut -c -$LENGTH`
echo hashcash -mb$STRENGTH $challenge

echo "hashcash token: "
read token
if [ `expr "$token" : "^[a-zA-Z0-9\+\_\.\:\/]\{52\}$"` -eq 52 ]; then
    hashcash -cdb$STRENGTH -f /tmp/hashcash.sdb -r $challenge $token 2> /dev/null
    if [ $? -eq 0 ]; then
        echo "[+] Correct"
    else
        echo "[-] Wrong"
        exit
    fi
else
    echo "[-] Wrong"
    exit
fi

cd /home/ubuntu/driver4b/build/qemu
timeout --foreground 300 qemu-system-x86_64 \
    -m 64M \
    -nographic \
    -kernel bzImage \
    -initrd rootfs.cpio \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on nokaslr" \
    -no-reboot \
    -cpu kvm64 \
    -monitor /dev/null \
    -net nic,model=virtio \
    -net user
