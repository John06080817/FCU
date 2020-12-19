.globl pin0
.sdata
pin0: word 1
.globl toggle
.text
.text
toggle:
LDR R10, R0, R1
LD R8, R0, pin0
XOR R10, R10, R8
STR R10, R0, R1
L.1:
RET
