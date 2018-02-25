import curses
import binascii
import os
import math
from curses import ascii

def hex_edit(filepath):
    filesize = os.path.getsize(filepath)
    rows = math.ceil(filesize/16)
    with open(filepath,'rb') as f:
        data = f.read()
    print(len(data),filesize)
    scr = curses.initscr()
    offsetdisplay = curses.newpad(100,11)
    hexdisplay = curses.newpad(100,33)
    bytedisplay = curses.newpad(100,16)
    bitsdisplay = curses.newwin(2,8,10,40)
    draw_offs_display(offsetdisplay,rows)
    draw_hex_display(hexdisplay,data)
    draw_byte_display(bytedisplay,data)
    


def draw_offs_display(offsd,rows):
    offsd.addstr("- offset -")
    for i in range(rows-1):
        offsd.addstr(i+1,0,"{0:#0{1}x}".format(i<<4,10))
    offsd.refresh(0,0,1,0,20,11)

def draw_hex_display(hexd,data):
    for i in range(16):
        hexd.addstr(" {0:X}".format(i))
        #https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
    hexd.addstr(binascii.hexlify(data).decode('ascii'))
    hexd.refresh(0,0,1,12,20,43)

def draw_byte_display(byted,data):
    for  i in range(16):
        byted.addstr("{0:X}".format(i))
    for i in range(len(data)):
        if(ascii.isgraph(data[i])):
            byted.addch(data[i])
        else:
            byted.addch('.')
    byted.refresh(0,0,1,45,20,62)

                     
    
