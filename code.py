"""
CircuitPython move text on TFT with track ball demo
Requires Feather with TFT like https://www.adafruit.com/product/5300 and 
https://wiki.seeedstudio.com/Grove-Mini_Track_Ball/
"""

import board
import time
import btc_grove_trackball
import terminalio
import displayio
from adafruit_display_text import bitmap_label

gr = displayio.Group()
t = bitmap_label.Label(terminalio.FONT, text="BTc", scale=3)
t.x = 10
t.y = 50
board.DISPLAY.show(gr)
gr.append(t)

i2c = board.I2C()

print("starting")    
tb = btc_grove_trackball.GroveTrackball(i2c)


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
minx = 0
maxx = 220
miny = 0
maxy = 150
lm = 0

while True:
    m = tb.motion()
    if m[2] > 0:
        t.x = constrain(t.x - 5,minx,maxx)
    if m[3] > 0:
        t.x = constrain(t.x + 5, minx, maxx)
    if m[0] > 0: 
        t.y = constrain(t.y - 5, miny, maxy)
    if m[1] > 0:
        t.y = constrain(t.y + 5, miny, maxy)
    if m[4] > 0:
        lm = (lm + 1) % 12
        tb.led(lm)
    time.sleep(.1)



