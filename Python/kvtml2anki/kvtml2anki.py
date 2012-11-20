#!/use/bin/python
# -*- coding: utf-8 -*-

import sys
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

def main(file_name):
    tree = ET.ElementTree(file=file_name)

#    up = [] # List of objects to place on top of the card
#    down = [] # List of objects to place on buttom of the card

    up = ""
    down = ""
    
    # translation with id 0 is top of the card and with id 1 is buttom of it.
    for elem in tree.iterfind('entries/entry/translation'):
        # In the previous version I used an astrik sign to ge all
        # items in a element. But if there was an element without
        # sound or image that solution would generate brokened out
        # put. In this solution I'll check every item and if they
        # exists then I'll add them to the output string.
        for item in elem.iterfind('text'):
            if elem.attrib['id'] == '0':
                up = item.text
            else:
                down = item.text
        if elem.iterfind('sound'):
            for item in elem.iterfind('sound'):
                up = up + "[sound:" + item.text +"]"
        if elem.iterfind('image'):
            for item in elem.iterfind('image'):
                down = "<img src='" + item.text + "'/><br />" + down
        print up + ";" + down
                
if __name__ == '__main__':
    # check for cmmand line arguments
    if len(sys.argv) < 2:
        print "Usage: python %s example.kvtml" % sys.argv[0]
    else:
        main(sys.argv[1])