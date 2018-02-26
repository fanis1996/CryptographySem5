#!/bin/python
import curses
import binascii
import os
import sys
import math
from curses import ascii

__BLOCK_S = 16
__OFFSET_PAD_W = 10
__HEX_PAD_W = __BLOCK_S * 3
__BYTE_PAD_W = __BLOCK_S

def hex_edit(filepath):
    x = 0
    y = 1
    with open(filepath,'rb') as f:
        data = f.read()
    rows = math.ceil(len(data)/ __BLOCK_S)
    Trows, Tcolumns = [int(s) for s in os.popen('stty size', 'r').read().split()]
    scr = curses.initscr()
    curses.noecho()
    offsetdisplay = curses.newpad(Trows,__OFFSET_PAD_W)
    hexdisplay = curses.newpad(Trows, __HEX_PAD_W)
    asciidisplay = curses.newpad(Trows, __BYTE_PAD_W)
    asciidisplay.keypad(True)
    asciidisplay.idlok(True)
    asciidisplay.scrollok(True)
    draw_offs_display(offsetdisplay,rows)
    draw_hex_display(hexdisplay,data)
    draw_byte_display(asciidisplay,data)
    curses.doupdate()
    while 1:
        c = asciidisplay.getch()
        if c == ord('q'):
            #save and exit
            with open(filepath,'wb') as f:
                f.write(data)
            break
        elif c in [curses.KEY_RIGHT, ord('l')] and x<__BYTE_PAD_W-1:
            hexdisplay.chgat(y,3*x,2,)
            x+=1
        elif c in [curses.KEY_LEFT, ord('h')] and x>0:
            hexdisplay.chgat(y,3*x,2,)
            x-=1
        elif c in [curses.KEY_UP, ord('k')] and y>1:
            hexdisplay.chgat(y,3*x,2,)
            y-=1
        elif c in [curses.KEY_DOWN, ord('j')] and y<Trows-1:
            hexdisplay.chgat(y,3*x,2,)
            y+=1
        elif c in [10, ord('i')]:
            #edit
            bitsdisplay = curses.newwin(1,9,0,16)
            bitsdisplay.keypad(True)
            bitsdisplay.addstr('{0:08b}'.format(data[x+(y-1)*__BLOCK_S]))
            bitsdisplay.move(0,0)
            bitsdisplay.refresh()
            b = bytearray(data)
            xb = 0
            while 1:
                c = bitsdisplay.getch()
                if c in [10, 27, ord('i'), ord('q')]:
                    break
                elif c in [ord(' '), ord('c'), ord('~')]:
                    #flip bit
                    bitsdisplay.erase()
                    b[x+(y-1)*__BLOCK_S] ^=1<<(7-xb)
                    bitsdisplay.addstr('{0:08b}'.format(b[x+(y-1)*__BLOCK_S]))
                    bitsdisplay.refresh()
                elif c in [curses.KEY_LEFT, ord('h')] and xb>0:
                    #move left
                    xb-=1
                elif c in [curses.KEY_RIGHT, ord('l')] and xb<7:
                    #move right
                    xb+=1
                bitsdisplay.move(0,xb)
                bitsdisplay.refresh()
            bitsdisplay.erase()
            bitsdisplay.refresh()
            data = bytes(b)
            draw_hex_display(hexdisplay,data)
            draw_byte_display(asciidisplay,data)

        hexdisplay.chgat(y,3*x,2,curses.A_STANDOUT)
        hexdisplay.noutrefresh(0,0,1, __OFFSET_PAD_W + 2,30, __OFFSET_PAD_W + 2 + __HEX_PAD_W)
        asciidisplay.move(y,x)
        asciidisplay.noutrefresh(0,0,1,__OFFSET_PAD_W + 2 + __HEX_PAD_W + 2, 30, __OFFSET_PAD_W +2 + __HEX_PAD_W + 2 + __BYTE_PAD_W)
        curses.doupdate()

    curses.endwin()

def draw_offs_display(offsd,rows):
    offsd.addstr("- offset -")
    for i in range(rows):
        offsd.addstr("{0:#0{1}x}".format(i * __BLOCK_S,10))
    offsd.noutrefresh(0,0,1,0,30, __OFFSET_PAD_W)

def draw_hex_display(hexd,data):
    hexd.move(0,0)
    for i in range( __BLOCK_S):
        hexd.addstr("{0:2X} ".format(i))
        #https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
    hexdata = binascii.hexlify(data).decode('ascii')
    hexd.addstr(' '.join(hexdata[i:i+2] for i in range(0, len(hexdata), 2)))
    hexd.noutrefresh(0,0,1, __OFFSET_PAD_W + 2,30, __OFFSET_PAD_W + 2 + __HEX_PAD_W)

def draw_byte_display(asciidisplay,data):
    asciidisplay.move(0,0)
    for  i in range(__BLOCK_S):
        asciidisplay.addstr("{0:X}".format(i))
    for i in range(len(data)):
        if(ascii.isgraph(data[i])):
            asciidisplay.addch(data[i])
        else:
            asciidisplay.addch('.')
    asciidisplay.move(1,0)
    asciidisplay.noutrefresh(0,0,1,__OFFSET_PAD_W + 2 + __HEX_PAD_W + 2, 30, __OFFSET_PAD_W +2 + __HEX_PAD_W + 2 + __BYTE_PAD_W)

if __name__ == "__main__":
    hex_edit(sys.argv[1])
