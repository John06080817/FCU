.globl dir
.sdata
dir: word 16384
.globl led
.sdata
led: word 16388
.globl main
.text
.text
main:
LDI R8, R0, -16
ADD SP, SP, R8
LD R10, R0, dir
STR R0, R0, R10
LD R10, R0, led
LDI R8, R0, 1
STR R8, R0, R10
JMP L.3
L.2:
LD R1, R0, led
CALL toggle
MOV R8, R0
L.5:
MOV R9, R0
L.9:
L.10:
LDI R9, R9, 1
LDI R10, R0, 47
CMP R9, R10
JLT L.9
L.6:
LDI R8, R8, 1
LDI R10, R0, 32767
CMP R8, R10
JLT L.5
L.3:
JMP L.2
L.1:
LDI R8, R0, 16
ADD SP, SP, R8
RET
