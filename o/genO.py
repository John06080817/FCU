# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:56:28 2020

@author: ce216
"""
f1 = open('D:\\python\\.o\\temp0.s', 'r')
f2 = open('D:\\python\\.o\\temp0.temp', 'w')

t = f1.readlines()

text = ''
data = ''
label = ''
globl = 0
sdata = 0
textstart = 0
for i in t:
    if '.globl' in i:
        globl = 1
        sdata = 0
        textstart = 0
        temp = i.split(' ')
        label += temp[1]
    elif globl == 1:
        if '.sdata' in i:
            sdata = 1
            globl = 0
        else:
            textstart = 1
            globl = 0
            text += i
    elif sdata == 1:
        data += i
    elif textstart == 1:
        if 'CALL' in i:
            temp = i.split(' ')
            if temp[1] not in label:
                label += temp[1]
        if '.frame' not in i:
            text += i

f2.write('.text\n' + text + '.data\n' + data + '.label\n' + label)
f1.close()
f2.close()