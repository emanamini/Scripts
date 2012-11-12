#!/use/bin/python
# -*- coding: utf-8 -*-

import sys
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

def main(file_name):
    tree = ET.ElementTree(file=file_name)

    up = [] # List of objects to place on top of the card
    down = [] # List of objects to place on buttom of the card

    # translation with id 0 is top of the card and with id 1 is buttom of it.
    for elem in tree.iterfind('entries/entry/translation'):
        # to export all sub entry in translations I used astrik ;-)
        for item in elem.iterfind('*'):
            if elem.attrib['id'] == '0':
                up.append(item.text)
            else:
                down.append(item.text)

    output = '' # Final generated string. it'll print on stdout.

    # Loop on generated list (up, down) every two step:
    for i in range(0, len(up), 2):
        # cut / from the media paths. it's lasy style ;-)
        sound = up[i+1].find('/')
        image = down[i+1].find('/')
        output += up[i] + "[sound:" + up[i+1][sound+1:] + "];<img src='" + down[i+1][image+1:] + "'/><br />" + down[i].encode('utf-8') + "\n"
        print output

if __name__ == '__main__':
    # check for cmmand line arguments
    if len(sys.argv) < 2:
        print "Usage: python %s example.kvtml" % sys.argv[0]
    else:
        main(sys.argv[1])