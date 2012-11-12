#!/usr/bin/python

import sys

if len(sys.argv) < 2:
    print "Usage: python xterm_to_terminator.py XResources_color_scheme"
    sys.exit(1)

input_file = open(sys.argv[1]).readlines()

foreground_color = ""
background_color = ""
for line in input_file:
    if line.find("foreground:") != -1:
        find_color = line.find("#")
        foreground_color = line[find_color:].strip()
    if line.find("*background:") != -1:
        find_color = line.find("#")
        background_color = line[find_color:].strip()
    if line.find("!") != -1:
        input_file.remove(line)
        
new_list = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '' ]
for line in input_file:
    color_index = line.find("color")
    colon_index = line.find(":")
    number = line[color_index+5:colon_index]

    number_sign = line.find("#")
    color_hex = line[number_sign:]

    if len(number)<=2 and len(number)>0:
        new_list[int(number)] = color_hex.strip()

palette = ""
for color in new_list:
    palette = palette + color + ":"
print "palette = " + "\"" + palette[:-1] + "\""
print "foreground_color = " + "\"" +  foreground_color + "\""
print "background_color = " + "\"" +  background_color + "\""
