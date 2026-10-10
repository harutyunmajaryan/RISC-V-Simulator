

li x1,4    ;x1 = radius = 4cm
li x2,3    ;x2 = pi = 3
li x3,1    ;x3 = area = 1

j calc_area_of_circle

calc_area_of_circle:
mul x3,x3,x2           ;area = area * pi
mul x3,x3,x1           ;area = area * radius
mul x3,x3,x1           ;area = area * radius
j print


print:
;area = pi * r * r

.text
.globl main
;1. Load print integer service code into a7
li a7, 1

;2. Load the number 10 into a0
mv a0,x3       ;a0 = x3 = pi * r^2

;3. Make the system call to print
ecall

;4. Exit program cleanly
li a7, 10
ecall
