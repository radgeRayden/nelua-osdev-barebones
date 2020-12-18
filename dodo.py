#!/usr/bin/env python

cc = "~/.local/opt/cross/bin/i686-elf-gcc"
qemu = "qemu-system-i386"

def task_build():
    boot_cmd = "nasm -felf32 boot.s -o boot.o"
    nelua_cmd = "nelua -c main.nelua --cpu-bits=32 --release"
    gcc_cmd = f"{cc} -c ./nelua_cache/main.c -o kernel.o -ffreestanding"
    link_cmd = f"{cc} -T linker.ld -o isodir/boot/image.bin -ffreestanding -O2 -nostdlib boot.o kernel.o -lgcc"
    grub_cmd = "grub-mkrescue -o radgeos.iso isodir"
    return {
        'actions': [boot_cmd, nelua_cmd, gcc_cmd, link_cmd, grub_cmd],
        'targets': ["radgeos.iso"]
    }

def task_launch():
    return {
        'actions': [f"{qemu} -cdrom radgeos.iso"],
        'file_dep': ["radgeos.iso"],
        'uptodate': [False]
    }
