#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author ervin

import sys
import os
import chardet


def main():
    source_path = sys.argv[1]
    # read content
    f = open(source_path, "r")
    content = f.read()
    f.close()
    
    # rename to bak file
    file_name = source_path + ".bak"
    os.rename(source_path, file_name)
    
    # dectet code set
    code_set = chardet.detect(content)
    encoding = code_set['encoding']
    utf_8_str = content.decode(encoding).encode("utf-8")
    f = open(source_path, "w")
    f.write(utf_8_str)
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        name = os.path.basename(sys.argv[0])
        print "Usage: {0} /path/to/file".format(name)
        exit(0)
    main()