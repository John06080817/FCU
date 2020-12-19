# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:13:46 2020

@author: ce216
"""
import os
import sys
import re
import pickle
def opCreate(t):
    opTable = {}
    for i in t:
        qqq = re.split(r'\s',i)
        qqq = list(filter(None, qqq))
        opTable[qqq[0]] = qqq[1:3]
    return opTable
        
def parse1(t):
    symbolTable = []
    dataTable = []
    labelTable = {}
    dataIndex = False
    globalIndex = False
    textIndex = False
    
    for i in t:
        if '.globl' in i:
            globalIndex = True
            dataIndex = False
            textIndex = False
        elif globalIndex:
            if '.data' in i or '.sdata' in i:
                dataIndex = True
                globalIndex = False
            elif '.text' in i:
                textIndex = True
                globalIndex = False
        elif '.' not in i[0]:
            if ':' in i:
                Index = i.index(':')
                if dataIndex:
                    labelTable[i[0:Index]] = ['data']
                elif textIndex:
                    labelTable[i[0:Index]] = ['text']
            if dataIndex:
                qqq = re.split(r':|,|\s',i)
                qqq = list(filter(None, qqq))
                dataTable.append(qqq)
            elif textIndex:
                qqq = re.split(r':|,|\s',i)
                qqq = list(filter(None, qqq))
                symbolTable.append(qqq)
    return symbolTable, dataTable, labelTable

def calLabelAddr(symbolTable, dataTable, labelTable):
    addr = 0
    for i in symbolTable:
        if i[0] in opTable:
            addr += 4
        else:
            labelTable[i[0]].append(addr)            
    for i in dataTable:
        labelTable[i[0]].append(addr)
        addr += 4
    '''
    for i in symbolTable:
        if i[0] in labelTable.keys():
            symbolTable.remove(i)
    '''
            

def genMachineCode(symbolTable, dataTable, labelTable):
    regVal = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11, 'SW':12, 'SP':13, 'LR':14, 'PC':15 }
    addrCount = 0
    machineCode = []    
    for i in symbolTable:
        if i[0] in labelTable.keys():
            continue
        if opTable[i[0]][1] == '1':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            addrCount += 4
        elif opTable[i[0]][1] == '2':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            addrCount += 1
            if i[1] in labelTable:
                labelTable[i[1]].append([0,addrCount])
            else:
                labelTable[i[1]] = ['unknown']
                labelTable[i[1]].append([0,addrCount])
            addrCount += 3
        elif opTable[i[0]][1] == '3':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            machineCode[-1] += regVal[i[1]]<<20
            addrCount += 4
        elif opTable[i[0]][1] == '4':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            machineCode[-1] += regVal[i[1]]<<20
            machineCode[-1] += regVal[i[2]]<<16
            addrCount += 4
        elif opTable[i[0]][1] == '5':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            machineCode[-1] += regVal[i[1]]<<20
            machineCode[-1] += regVal[i[2]]<<16
            addrCount += 2
            if i[3] in labelTable:
                labelTable[i[3]].append([0,addrCount])
            else:
                machineCode[-1] += int(str(hex(int(i[3]) & (2**16-1))),16)
            addrCount += 2
        elif opTable[i[0]][1] == '6':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            machineCode[-1] += regVal[i[1]]<<20
            machineCode[-1] += regVal[i[2]]<<16
            machineCode[-1] += regVal[i[3]]<<12
            addrCount += 4
        elif opTable[i[0]][1] == '7':
            machineCode.append(int(opTable[i[0]][0],16)<<24)
            machineCode[-1] += regVal[i[1]]<<20
            machineCode[-1] += regVal[i[2]]<<16
            machineCode[-1] += int(str(hex(int(i[3]) & (2**5-1))),16)
            addrCount += 4
    dataCount = 0
    dataCode = [addrCount]
    for i in dataTable:
        dataCode.append(int(i[-1]))
        dataCount += 4
    return machineCode, dataCode, [addrCount, dataCount]

def printMachineCode(machineCode, dataCode, count):
    print(format(0,'04x') + ' ' + format(count[0],'02x'))
    for i in machineCode:
        print(format(i,'08x'))
    print(format(dataCode[0],'04x') + ' ' + format(count[1],'02x'))
    for i in dataCode[1:]:
        print(format(i,'08x'))

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('請輸入需要組譯之檔案')
        sys.exit(0)
    #read opTable
    nowPath = os.getcwd()
    file = open(nowPath + '\op.txt', 'r')
    t = file.readlines()
    opTable = opCreate(t)
    file.close()
    
    #read and parse
    f1 = open(nowPath + '\\' + sys.argv[1], 'r')
    t = f1.readlines()
    symbolTable, dataTable, labelTable = parse1(t)
    f1.close()
    
    #cal label address
    calLabelAddr(symbolTable, dataTable, labelTable)
    
    #gen machine code
    machineCode, dataCode, count = genMachineCode(symbolTable, dataTable, labelTable)
    
    #test print
    printMachineCode(machineCode, dataCode, count)
    
    #save data
    output = {'text': [0, count[0], machineCode], 'data': [dataCode[0], count[1], dataCode[1:]], 'label': labelTable}
    file = open(nowPath + '\\' + sys.argv[1][:-1] + 'o', 'wb')
    pickle.dump(output, file)
    file.close()
    '''
    file = open('D:\\python\\o\\c1.o', 'rb')
    test = pickle.load(file)
    file.close()
    '''