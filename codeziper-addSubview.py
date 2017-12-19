#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("srcdir", help="specify the src directory")
args = parser.parse_args()

srcdir = args.srcdir
if os.path.exists(srcdir):
    pass
else:
    print " not exist:%s" % srcdir
    sys.exit()

#[_panelView addSubview:item.redPoint]

projectfilelist = ["QQMainProject/QQMainProject.xcodeproj/project.pbxproj"]

def removeCommentLine(content):
    result = re.sub(r'^\s*\/\/.*?$','',content,flags=re.M) #multiline mode: ^...$ match one line
    result = re.sub(r'\/\*.*?\*\/','',result,flags=re.S)
    return result

def scansrc():
    list_sourcecodes = []
    #read project file
    projectfilecontent = ""
    for path in projectfilelist:
        fullpath = os.path.join(srcdir,path)
        projectfile = open(fullpath,"r")
        projectfilecontent = projectfilecontent + projectfile.read()
        projectfile.close()
    
    #get src file list
    filterFiles = ["CodeZipper.m"]
    excludeDirs = set(["QQNotificationService", "QQNotificationContent", "QQSiriIntents", "QQSiriIntentsUI", "QQShare"])
    arrowExtension = [".mm",".m"]
    for root, dirs, files in os.walk(srcdir, topdown=False):
        stop = False
        for excludeDir in excludeDirs:
            if excludeDir in root:
                stop = True
                break
        if stop:
            continue
        for name in files:
            #print(os.path.join(root, name))
            if not name in filterFiles:
                fileName, fileExtension = os.path.splitext(name)
                if fileExtension in arrowExtension:
                    if name in projectfilecontent:
                        list_sourcecodes.append(os.path.join(root, name))
    return list_sourcecodes

def findtargetstring(content):
    content1 = removeCommentLine(content)
    matches = re.findall('\[[^\s]*?\saddSubview:[^\s]*?\]', content1)
    return matches

def replacecontent(content, matches):
    for match in matches:
        matchobj = re.search('\[(.*?)\saddSubview:(.*?)\]', match)
        receiver = matchobj.group(1).strip()
        subview = matchobj.group(2).strip()
        #check receiver grammar
        if receiver == '' or receiver.count('[') != receiver.count(']') or receiver == 'super':
            continue
        if subview == '' or subview.count('[') != subview.count(']'):
            continue
        zipcode = "CZ_AddSubview("+receiver+", "+subview+")"
#        print match
#        print zipcode
        content = content.replace(match, zipcode)
    return content

print "scanning source files...."
arrowExtension = [".mm",".m"]
count = 0
modifycount = 0
list_sourcecodes = scansrc()

print "found %d file to scan...." % len(list_sourcecodes)

for file in list_sourcecodes:
    replacedcontent = None
    with open(file) as f:
        content = f.read()
        matches = findtargetstring(content)
        if len(matches):
            matches = list(set(matches))#remove redundant
            replacedcontent = replacecontent(content, matches)
                
    if replacedcontent:
        with open(file, 'w') as f:
            f.write(replacedcontent)
            modifycount = modifycount + 1
    count = count + 1
    sys.stdout.write("\r%s files scanned       " % count)

print "\nmodified %d files." % modifycount

