li x3,2   ; x3 = 2
li x4,5   ; x4 = 5

j main     ;jumps to main


main:
add x5,x3,x4    ;x5 = x3 + x4 = 7
addi x5,x5,3    ;x5 = x5 + 3 = A(10)
sra x6,x5,1      ;x6 = x5 / 2 = 5


li x7,5     ;x7 = 5

label:
beq x6,x7,exit   ;if x6=x7 then exit
sll x8,x6,1      ;else x8 = x6 * 2 = 10
j exit

exit:
;exits the program entirely

