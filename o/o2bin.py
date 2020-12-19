# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:22:31 2020

@author: ce216
"""
import sys, os
import pickle

#read .o file
if len(sys.argv) <= 3:
    print('請輸入需要在鏈結之檔案')
    sys.exit(0)
nowPath = os.getcwd()
comb = []
for i in sys.argv[1:-1]:
    file1 = open(nowPath + '\\' + i, 'rb')
    test = pickle.load(file1)
    comb.append(test)
    file1.close()

#calcu address
startAddr = 84
for i in comb:
    addAddr = startAddr - i['text'][0]
    i['text'][0] = startAddr
    startAddr += i['text'][1]
    for j in i['label']:
        if i['label'][j][0] == 'text':
            i['label'][j][1] += addAddr
        if len(i['label'][j])>2:
            for k in i['label'][j][2:]:
                k[0] += addAddr
        if i['label'][j][0] == 'unknown':
            for k in i['label'][j][1:]:
                k[0] += addAddr
for i in comb:
    addAddr = startAddr - i['data'][0]
    i['data'][0] = startAddr
    startAddr += i['data'][1]
    for j in i['label']:
        if i['label'][j][0] == 'data':
            i['label'][j][1] += addAddr

#combine label
allLabel = {}
for i in comb:
    for j in i['label']:
        if i['label'][j][0] != 'unknown':
            allLabel[j] = i['label'][j]
for i in comb:
    for j in i['label']:
        if i['label'][j][0] == 'unknown':
            for k in i['label'][j][1:]:
                allLabel[j].append(k)
              
#gen bootloader
bootloader = [0x26000048]
if 'ISR_GPIO' in allLabel.keys():
    temp = 0x26000000 + allLabel['ISR_GPIO'][1]
else:
    temp = 0
bootloader.append(temp)
if 'ISR_UART' in allLabel.keys():
    temp = 0x26000000 + allLabel['ISR_UART'][1]
else:
    temp = 0
bootloader.append(temp)
if 'ISR_TIM1' in allLabel.keys():
    temp = 0x26000000 + allLabel['ISR_TIM1'][1]
else:
    temp = 0
bootloader.append(temp)
for i in range(15):
    bootloader.append(0xffffffff)
bootloader.append(0x08d04000)
temp = 0x26000000 + allLabel['main'][1] - 0x54
bootloader.append(temp)

#label insert machinecode
for i in allLabel:
    if len(allLabel[i])>2:
        for j in allLabel[i][2:]:
            for k in comb:
                if k['text'][0] == j[0]:
                    if allLabel[i][0] == 'data':
                        k['text'][2][int(j[1]//4)] += allLabel[i][1]
                    elif allLabel[i][0] == 'text':
                        k['text'][2][int(j[1]//4)] += int(str(hex(allLabel[i][1]-(j[0] + j[1] + 3) & (2**24-1))),16)
    
#print result
for i in comb:
    for j in i['text'][2]:
        print(format(j, '08x'))
for i in comb:
    for j in i['data'][2]:
        print(format(j, '08x'))
                    
#gen .bin
output = open(nowPath + '\\' + sys.argv[-1] + '.bin', 'wb')
for i in bootloader:
    int_bytes = i.to_bytes(4, 'big')
    output.write(int_bytes)
for i in comb:
    for j in i['text'][2]:
        int_bytes = j.to_bytes(4, 'big')
        output.write(int_bytes)
for i in comb:
    for j in i['data'][2]:
        int_bytes = j.to_bytes(4, 'big')
        output.write(int_bytes)
output.close()
                    

    
                    
                    
                    