li x1,10   ;x1 = 10
li x2,10    ;x2 = 10
li x3,-1     ;x3 = -1
j loop

loop:
beq x1,x2,decrement        ;if x1 = x2, then jump to decrement
j exit                     ;jump to exit

decrement:
add x1,x1,x3            ;x1 = x1 - x3,x1 = 9
beq x1,x0,exit          ;if x1 = x0 then exit
j decrement             ;otherwise loop again


exit:
;exits the program entierly


