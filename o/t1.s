.globl a
.sdata
a: word 3
.globl f1
.text
.text
f1:
.frame SP, 8
LDI R8, R0, -8
ADD SP, SP, R8
LDI R10, R0, 4
ST R10, SP, 4
LD R11, SP, 4
L.1:
LDI R8, R0, 8
ADD SP, SP, R8
RET
.globl main
.text
main:
.frame SP, 24
LDI R8, R0, -24
ADD SP, SP, R8
CALL f1
LD R8, R0, a
ADD R10, R11, R8
ST R10, SP, 20
MOV R11, R0
L.2:
LDI R8, R0, 24
ADD SP, SP, R8
RET
