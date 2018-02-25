import curses
import binascii
import os
import math
from curses import ascii

__BLOCK_S = 16
__OFFSET_PAD_W = 10
__HEX_PAD_W = __BLOCK_S * 3
__BYTE_PAD_W = __BLOCK_S

def hex_edit(filepath):
    with open(filepath,'rb') as f:
        data = f.read()
    rows = math.ceil(len(data)/ __BLOCK_S)
    Trows, Tcolumns = [int(s) for s in os.popen('stty size', 'r').read().split()]
    scr = curses.initscr()
    offsetdisplay = curses.newpad(Trows,__OFFSET_PAD_W)
    hexdisplay = curses.newpad(Trows, __HEX_PAD_W)
    bytedisplay = curses.newpad(Trows, __BYTE_PAD_W)
    draw_offs_display(offsetdisplay,rows)
    draw_hex_display(hexdisplay,data)
    draw_byte_display(bytedisplay,data)
    while 1:
        c = bytedisplay.getch()
        if c == ord('q'):
            break
    curses.endwin()

def draw_offs_display(offsd,rows):
    offsd.addstr("- offset -")
    for i in range(rows):
        offsd.addstr("{0:#0{1}x}".format(i * __BLOCK_S,10))
    offsd.refresh(0,0,1,0,30, __OFFSET_PAD_W)

def draw_hex_display(hexd,data):
    for i in range( __BLOCK_S):
        hexd.addstr("{0:2X} ".format(i))
        #https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
    hexdata = binascii.hexlify(data).decode('ascii')
    hexd.addstr(' '.join(hexdata[i:i+2] for i in range(0, len(hexdata), 2)))
    hexd.refresh(0,0,1, __OFFSET_PAD_W + 2,30, __OFFSET_PAD_W + 2 + __HEX_PAD_W)

def draw_byte_display(byted,data):
    for  i in range(__BLOCK_S):
        byted.addstr("{0:X}".format(i))
    for i in range(len(data)):
        if(ascii.isgraph(data[i])):
            byted.addch(data[i])
        else:
            byted.addch('.')
    byted.refresh(0,0,1,__OFFSET_PAD_W + 2 + __HEX_PAD_W + 2, 30, __OFFSET_PAD_W +2 + __HEX_PAD_W + 2 + __BYTE_PAD_W)

hex_edit('/tmp/tete')
