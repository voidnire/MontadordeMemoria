.code 

not r2, r2
data r0, 0x01
add r0, r2

st r1, r2

add r0, r1
cmp r3, r1
jcaez 0x06
jmp 0x0e

.data 
word 15 ; This is an inline comment 

word 0xcd
