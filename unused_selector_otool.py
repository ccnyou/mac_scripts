#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import argparse

blacklist = ['.cxx_construct', '.cxx_destruct']

parser = argparse.ArgumentParser()
parser.add_argument("-a",
                    "--arm64",
                    help="also calculate arm64 size, will be slower.",
                    action="store_true",
                    dest="a",
                    default=False)
args = parser.parse_args()

print "scanning selector list...."

f = open("QQMainProject-LinkMap-arm64.txt", "r")
content_arm64 = f.read()
f.close()

selector_list = []
selector_pattern = "(0x\w+)\t\[\s*(\d+)\]\s[+|\-]\[(\w+\s(.+))\]\n"
match_list = re.findall(selector_pattern, content_arm64)
index = 0
for match in match_list:
    index += 1
    size_in_byte = str(int(match[0], 16))
    target_id = match[1]
    class_and_selector = match[2]
    selector = match[3]
    target_pattern = "\n\[\s*" + target_id + "\]\s.+\/(.+)"
    result = re.search(target_pattern, content_arm64)
    if not result:
        print "match pattern fail, match = "
        print match
        continue
    target_name = result.group(1)
    selector_list.append((target_name, size_in_byte, class_and_selector, selector))
    sys.stdout.write("\r%d selector scaned       " % index)

print "\ndone scanning selector list...."

print "scanning for unused selectors...."
f = open("selrefs.txt", "r")
content = f.read()
f.close()

f1 = open("result.txt", "w")
f2 = open("staticlibresult.txt", "w")

if args.a:
    f1.write("objectfilename\tsizeinbytearmv7\tsizeinbytearm64\tselectorname\n")
else:
    f1.write("objectfilename\tsizeinbytearmv7\tselectorname\n")

index = 0
for selector in selector_list:
    index += 1
    object_file_name = selector[0]
    size_in_byte_armv7 = selector[1]
    class_and_selector = selector[2]
    selector_name = selector[3]
    if selector_name not in content and selector_name not in blacklist:
        if args.a:
            # search for size in arm64
            arm64pattern = "(0x\w+)\t\[\s*\d+\]\s[+|\-]\[" + class_and_selector + "\]\n"
            match_object_arm64 = re.search(arm64pattern, content_arm64)
            size_in_byte_arm64 = 0
            if match_object_arm64:
                size_in_byte_arm64 = str(int(match_object_arm64.group(1), 16))
            result = '\t'.join((object_file_name, size_in_byte_armv7, size_in_byte_arm64, selector_name)) + '\n'
        else:
            result = '\t'.join((object_file_name, size_in_byte_armv7, selector_name)) + '\n'
        if '(' in object_file_name:
            f2.write(result)
        else:
            f1.write(result)
    sys.stdout.write("\r%d selector scaned       " % index)
f1.close()
f2.close()
print "\ndone"
