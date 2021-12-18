import pyonfx as pkfx
import random

io = pkfx.Ass("test.ass")
opt = io
meta, styles, lines = io.get_data()
multi_color = ["&H197EFE&", "&H9812FC&", "&H6BE57E&", "&HECDE7D&", "&H36F8F0&", "&HDB34F1&"]

def get_color(in_slow:list, in_high:list):
    opt = []
    for c in in_high:
        if c not in in_slow:
            opt.append(c)
    return opt

def kfx1m(line, l, debug=False):
    if debug:
        for line in lines:
            l = line
    r = len(multi_color1) * 2 - 2
    blueBegin = 6
    l.layer = 1
    for i in range(1, r+1):
        if i % 2 != 0:
            timeIncre = (i // 2) * 120
            blurDecre = (i // 2) * 3
            l.start_time = line.start_time + timeIncre
            l.end_time   = l.start_time + 40
            blurBegin    = blueBegin - blurDecre
            blurEnd      = blurBegin - 1
            colorNum     = i // 2
            l.text = "{\\bord0\\blur%s\\c%s\\t(0,%s,\\c%s\\blur%s)}%s" % (blurBegin, multi_color1[colorNum], 40, multi_color1[colorNum+1], blurEnd, line.text)
        else:
            timeIncre = (i // 2) * 120 - 80
            blurDecre = (i // 2) * 3 - 2
            l.start_time = line.start_time + timeIncre
            l.end_time   = l.start_time + 80
            blurBegin    = blueBegin - blurDecre
            blurEnd      = blurBegin - 2
            colorNum     = i // 2
            l.text = "{\\bord0\\blur%s\\c%s\\t(0,%s,\\blur%s)}%s" % (blurBegin, multi_color1[colorNum], 80, blurEnd, line.text)
        opt.write_line(l)

def kfx2m(line, l, debug=False):
    if debug:
        for line in lines:
            l = line
    r = len(multi_color2) * 2 + 2
    l.layer = 1
    for i in range(1, r+1):
        if i % 2 != 0:
            timeIncre = (i // 2) * 120
            l.start_time = line.start_time + 240 + timeIncre
            l.end_time   = l.start_time + 80
            colorNum     = (i - 2) // 2
            if i == 1:
                l.text = "{\\c%s\\t(0,%s,\\c%s)}%s" % (multi_color1[len(multi_color1) - 1], 80, multi_color2[0], line.text)
            elif i == len(multi_color2) * 2 + 1:
                l.text = "{\\c%s\\t(0,%s,\\c%s}%s" % (multi_color2[len(multi_color2) - 1], 80, '&HFFFFFF&', line.text)
            else:
                l.text = "{\\c%s\\t(0,%s,\\c%s}%s" % (multi_color2[colorNum], 80, multi_color2[colorNum+1], line.text)
        else:
            timeIncre = (i // 2) * 120 - 40
            l.start_time = line.start_time + 240 + timeIncre
            colorNum     = (i - 2) // 2
            if i == r:
                l.end_time = line.end_time
                if l.end_time - l.start_time > 240:
                    l.text = "{\\fad(0,240)}%s" % (line.text)
                else: l.text = "{\\fad(0,%s)}%s" % ((l.end_time - l.start_time) * 0.1, line.text)
            else:
                l.end_time   = l.start_time + 40
                l.text = "{\\c%s}%s" % (multi_color2[colorNum], line.text)
        opt.write_line(l)

def shad(line, l, debug=False):
    if debug:
        for line in lines:
            l = line
    l.layer = 0
    l.start_time = line.start_time + 240
    if l.end_time - l.start_time - 440 > 240:
        l.text = "{\\an5\\pos(%.2f,%.2f)\\c&H702F2F&\\blur2\\fad(0,240)}%s" % (line.center+3, line.middle+3, line.text)
    else: l.text = "{\\an5\\pos(%.2f,%.2f)\\c&H702F2F&\\blur2\\fad(0,%s)}%s" % (line.center+3, line.middle+3, (l.end_time - l.start_time - 440) * 0.1, line.text)
    opt.write_line(l)

for line in lines:
    multi_color1 = random.sample(multi_color, 3)
    multi_color2 = get_color(multi_color1, multi_color)
    kfx1m(line, line.copy())
    kfx2m(line, line.copy())
    shad(line, line.copy())

opt.save()
opt.open_aegisub()