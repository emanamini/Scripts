#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import codecs
__version__ = "0.1"

def helpMessage():
    print "Usage: python chrvalidator.py -i INPUTFILE -[cuUd]"

def main():
    if len(sys.argv) < 2:
        helpMessage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:cuUd",
                                   ["help", "version", "input=", "output=", "characters",
                                    "unicode-code", "unicode-char", "do-validation"])
    except getopt.GetoptError, err:
        print str(err)
        helpMessage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMessage()
            sys.exit(0)
        if opt in ("-v", "--version"):
            print __version__
            sys.exit(0)
        if opt in ("-i", "--input"):
            input_file = arg
        if opt in ("-o", "--output"):
            output_file = arg
        if opt in ("-c", "--characters"):
            show_characters(input_file)
            sys.exit(0)
        if opt in ("-u", "--unicode-code"):
            show_unicode_code(input_file)
            sys.exit(0)
        if opt in ("-U", "--unicode-char"):
            replace_unicode_char(input_file)
            sys.exit(0)
        if opt in ("-d", "--do-validation"):
            do_validation(input_file)
            sys.exit(0)

def read_file(file_name):
    """A function to read the input file"""
    the_file = codecs.open(file_name, encoding="utf-8")
    return the_file

def show_characters(input_file):
    """Show all files content character by character (one character
    per line)

    """
    for line in read_file(input_file).readlines():
        for char in line:
            print char

def show_unicode_code(input_file):
    """Show all files content unicode number (one character per
    line)

    """
    for line in read_file(input_file).readlines():
        for char in line:
            print ord(char)

def replace_unicode_char(input_file):
    """Replace unicode numbers to characters (input has to have one
    code per line)

    """
    for line in read_file(input_file).readlines():
        print unichr(int(line)).encode('utf-8')

def do_validation(input_file):
    for line in read_file(input_file).readlines():
        for char in line:

            if ord(char) in (64343, 64344, 64345):
                char = "پ"
            elif ord(char) in (64379, 64380, 64381):
                char = "چ"
            elif ord(char) in (64395,):
                char = "ژ"
            elif ord(char) in (64399, 64400, 64401):
                char = "ک"
            elif ord(char) in (64403, 64404, 64405):
                char = "گ"
            elif ord(char) in (64509,):
                char = "ی"
            elif ord(char) in (64607, 64608, 64609, 64610):
                # This is arabic tashdid compund with fathe, zamme,
                # kasre. I cleaned them for now
                char = ""
            elif ord(char) in (65010,):
                char = "لله"
            elif ord(char) in (64153,):
                char = "آ"
            elif ord(char) in (65154, 65156):
                # These are "ﺂ" and "ﺄ"
                char = "أ"
            elif ord(char) in (65158, ):
                # This is "ﺆ"
                char = "ؤ"
            elif ord(char) in (65162, 65163, 65165):
                char = "ئ"
            elif ord(char) in (65166,):
                char = "ا"
            elif ord(char) in (65168, 65169, 65170):
                char = "ب"
            elif ord(char) in (65172,):
                char = "هٔ"
            elif ord(char) in (65174, 65175, 65176):
                char = "ت"
            elif ord(char) in (65178, 65179, 65180):
                char = "ث"
            elif ord(char) in (65182, 65183, 65184):
                char = "ج"
            elif ord(char) in (65186, 65187, 65188):
                char = "ح"
            elif ord(char) in (65190, 65191, 65192):
                char = "خ"
            elif ord(char) in (65194,):
                char = "د"
            elif ord(char) in (65196,):
                char = "ذ"
            elif ord(char) in (65198,):
                char = "ر"
            elif ord(char) in (65200,):
                char = "ز"
            elif ord(char) in (65202, 65203, 65204):
                char = "س"
            elif ord(char) in (65206, 65207, 65208):
                char = "ش"
            elif ord(char) in (65210, 65211, 65212):
                char = "ص"
            elif ord(char) in (65214, 65215, 65216):
                char = "ض"
            elif ord(char) in (65218, 65219, 65220):
                char = "ط"
            elif ord(char) in (65222, 65223, 65224):
                char = "ظ"
            elif ord(char) in (65226, 65227, 65228):
                char = "ع"
            elif ord(char) in (65230, 65231, 65232):
                char = "غ"
            elif ord(char) in (65234, 65235, 65236):
                char = "ف"
            elif ord(char) in (65238, 65239, 65240):
                char = "ق"
            elif ord(char) in (65246, 65247, 65248):
                char = "ل"
            elif ord(char) in (65250, 65251, 65252):
                char = "م"
            elif ord(char) in (65254, 65255, 65256):
                char = "ن"
            elif ord(char) in (65257, 65258, 65259, 65260):
                char = "ه"
            elif ord(char) in (65262,):
                char = "و"
            elif ord(char) in (65266, 65267, 65268):
                char = "ی"
            elif ord(char) in (65275, 65276):
                char = "لا"

            # To prevent  add space between characters  here in python
            # 2.7 this is the only way that is worked
            sys.stdout.softspace=False
            try:
                print char.encode("utf-8"), 
            except UnicodeDecodeError:
                print char,

if __name__ == "__main__":
    main()