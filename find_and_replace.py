# -*- coding: utf-8 -*-
import fileinput
import re
from tempfile import mkstemp
from shutil import move
from os import remove, close
import os

def main():
    folders = getFolderNames(r"C:\automation\tests");
 
    for folder in xrange(0, len(folders)):
        files = getFileNames(r"C:\automation\tests\%s" %folders[folder], ".py");
         
        for file in xrange(0, len(files)):
            findAndReplace(r"C:\automation\tests\%s" %folders[folder], files[file]);
        
def getFolderNames(root):           
    folders = [];
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            folders.append(item);
    return folders       

def getFileNames(folder, extension):
    names = [];
    for file_name in os.listdir(folder):
        if file_name.endswith(extension):
            names.append(file_name)
    return names

def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    remove(file_path)
    move(abs_path, file_path)
        
def findAndReplace(path, name):
    file_path = path + "\\" + name
    match_list = [];
    repl_list = [];
    with open(file_path, "r+") as f:
        for line in f:     
            for match in re.finditer('(type\(waitForObject\(.*?(.+?)\)\, )(.*?(.+?))\)', line, re.S):
                match_text = match.group();
                obj = match.group(2);
                input = match.group(3);
                repl_text = 'typeText('+ obj +', '+ input +')'
                match_list.append(match_text)
                repl_list.append(repl_text)
    print "    "
    print "In file path: %s" %file_path
    for item in xrange(0, len(match_list)):
        print '%s     replaced with     %s' %(match_list[item], repl_list[item])
        replace(file_path, match_list[item], repl_list[item])

if __name__ == '__main__':
    main()
