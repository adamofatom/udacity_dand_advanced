#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.
    
    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    with open(filename, 'r') as reader:
        filenum = -1
        writer = None
        for line in reader:
            if line.find('<?xml version="1.0" encoding="UTF-8"?>') != -1:
                if writer:
                    writer.close()
                filenum += 1
                writer = open("{}-{}".format(filename, filenum), 'w')
            writer.write(line)
        writer.close()

# #  from mentor
# def split_file(filename):
#     with open(filename) as infile:
#         n = -1 # 由于第一次遇到 '<?xml' 时会关闭文件，导致跳空一次
#                # 所以临时从 -1 开始，保证能从 0 正式开始
#         outfile = open('{}-{}'.format(filename, n), 'w') # 单独打开

#         for line in infile:
#             if line.startswith('<?xml'):
#                 # 每次切换步骤：关闭、+1、再打开
#                 outfile.close() 
#                 n += 1       
#                 outfile = open('{}-{}'.format(filename, n),'w')

#             outfile.write(line)
            
#         outfile.close() # 记得用完关闭


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()