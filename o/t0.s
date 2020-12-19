.globl a
.sdata
a: word 3
.globl f1
f1:
.frame SP, 8
LDI R8, R0, -8
ADD SP, SP, R8
LDI R10, R0, 4
ST R10, SP, -4+8
LD R11, SP, -4+8
L.1:
LDI R8, R0, 8
ADD SP, SP, R8
RET
.globl main
main:
.frame SP, 24
LDI R8, R0, -24
ADD SP, SP, R8
CALL f1
LD R8, R0, a
ADD R10, R11, R8
ST R10, SP, -4+24
MOV R11, R0
L.2:
LDI R8, R0, 24
ADD SP, SP, R8
RET
