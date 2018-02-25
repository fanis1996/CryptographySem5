import curses
import binascii
import os
import math
from curses import ascii

def hex_edit(filepath):
    with open(filepath,'rb') as f:
        data = f.read()
    rows = len(data)
    scr = curses.initscr()
    offsetdisplay = curses.newpad(rows+1,10)
    hexdisplay = curses.newpad(rows+1,32)
    bytedisplay = curses.newpad(rows+1,16)
    bitsdisplay = curses.newwin(2,8,10,40)
    draw_offs_display(offsetdisplay,rows)
    draw_hex_display(hexdisplay,data)
    draw_byte_display(bytedisplay,data)
    


def draw_offs_display(offsd,rows):
    offsd.addstr("- offset -")
    for i in range(rows):
        offsd.addstr("{0:#0{1}x}".format(i<<4,10))
    offsd.refresh(0,0,1,0,20,10)

def draw_hex_display(hexd,data):
    for i in range(16):
        hexd.addstr(" {0:X}".format(i))
        #https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
    hexd.addstr(binascii.hexlify(data).decode('ascii'))
    hexd.refresh(0,0,1,12,20,44)

def draw_byte_display(byted,data):
    for  i in range(16):
        byted.addstr("{0:X}".format(i))
    for i in range(len(data)):
        if(ascii.isgraph(data[i])):
            byted.addch(data[i])
        else:
            byted.addch('.')
    byted.refresh(0,0,1,45,20,62)

hex_edit('/home/fanis1996/Downloads/f1')

                     
    
