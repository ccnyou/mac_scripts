#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author ervin

import sys
import os


def is_file_contains_headers(file_path):
    if ".m" in file_path:
        return True
    if ".h" in file_path:
        return True
    return False


def is_line_code_contains_header(line_code):
    if "#import" in line_code:
        return True
    if "#include" in line_code:
        return True
    return False


def header_compare(left, right):
    if "<" in left and "<" in right:
        return len(left) - len(right)
    if "<" not in left and "<" not in right:
        return len(left) - len(right)
    if "<" in left:
        return -1
    return 1


def sort_header(file_path):
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    line_count = len(file_lines)

    begin_line = -1
    end_line = -1
    for i in range(0, line_count):
        line_code = file_lines[i]
        if is_line_code_contains_header(line_code):
            begin_line = i
            break

    if begin_line < 0:
        print "no headers found, file_path = " + file_path
        return

    for i in range(begin_line, line_count):
        line_code = file_lines[i]
        end_line = i
        if not is_line_code_contains_header(line_code):
            break

    headers = file_lines[begin_line:end_line]
    headers = sorted(headers, header_compare)
    file_lines[begin_line:end_line] = headers
    with open(file_path, "w") as f:
        f.writelines(file_lines)


def sort_files_headers(root, files):
    for f in files:
        file_path = os.path.join(root, f)
        if not is_file_contains_headers(file_path):
            continue
        print "processing " + file_path
        sort_header(file_path)


def main():
    source_path = sys.argv[1]
    list_dirs = os.walk(source_path)
    for root, dirs, files in list_dirs:
        sort_files_headers(root, files)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        name = os.path.basename(sys.argv[0])
        print "Usage: {0} /path/to/source".format(name)
        exit(0)
    main()
