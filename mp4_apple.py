#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

Set MP4 multi audio track alternate group for iOS/iTunes. To instead of "Dumpster.exe"

Usage: mp4_apple.py file.mp4

Author: squ@github
Version: 0.2

TODO: Add process for multi soft subtitle

"""

import sys;
from struct import unpack, calcsize, pack

def get_section(f, pos):
    struct_type = '>I4s'
    f.seek(pos)
    data = f.read(calcsize(struct_type))
    return unpack(struct_type, data)

def get_audio_trak(f):
    f.read(40)
    return unpack(">3H", f.read(6))

def main():
    argvLen = len(sys.argv);
    if argvLen < 2:
        print "Usage: mp4_apple.py file.mp4"
        exit(0)
    
    f = open(sys.argv[1], "rb+")
    try:
        count = 1
        pos = 0
        section_length, section_name = get_section(f, pos)

        if section_name != "ftyp":
            print section_name, "is not a valid head."
            exit(0)

        pos = f.tell()
        layer_index = 65535
            
        while section_name != 'mdat' and count < 20:
            count = count + 1
            pos = pos + section_length
            section_length,section_name = get_section(f, pos)
            if section_name == 'trak':
                layer, alternate_group, volumn = get_audio_trak(f)
                if volumn > 0:
                    print section_length, section_name, " -> ", "Layer:", layer, "Alternate group:", alternate_group, "Volumn:", volumn
                    if layer != layer_index or alternate_group != 1:
                        f.seek(f.tell()-6)
                        f.write(pack('>3H', layer_index, 1, 256))
                        print '...Fixed'
                    else:
                        print '...No need to fix'
                    layer_index = layer_index - 1
    finally:
        f.close()

if __name__=="__main__":
    main();