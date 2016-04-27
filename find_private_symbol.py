#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author ervinchen

import sys
import os
import subprocess


def is_file_contain_symbol(file_path, symbol):
    if ".m" in file_path:
        return False
    if ".h" in file_path:
        return False
    if ".png" in file_path:
        return False
    command_result = subprocess.Popen(["strings", file_path], stdout=subprocess.PIPE)
    strings = command_result.stdout.read()
    if symbol in strings:
        return True


def find_private_symbol(root, files, symbol, contain_symbol_files):
    for f in files:
        file_path = os.path.join(root, f)
        if is_file_contain_symbol(file_path, symbol):
            contain_symbol_files.append(file_path)


def main():
    import_path = sys.argv[1]
    symbol = sys.argv[2]
    contain_symbol_files = []
    list_dirs = os.walk(import_path)
    for root, dirs, files in list_dirs:
        find_private_symbol(root, files, symbol, contain_symbol_files)

    count = len(contain_symbol_files)
    if count == 0:
        print "未找到任何包含符号的文件"
        return 0

    print "找到" + str(count) + "个文件:"
    for f in contain_symbol_files:
        print f


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: find_private_symbol.py /path/to/import/ privateSymbol"
        exit(0)
    main()