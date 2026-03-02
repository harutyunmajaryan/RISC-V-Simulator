Bennett is a lightweight, visual RISC-V assembly simulator built with Python and Tkinter. It is designed to help students and developers visualize how the CPU state changes in real-time as instructions are executed.
Unlike traditional command-line simulators, Bennett provides a dual-view of registers (ABI and Hardware names) to help users master RISC-V calling conventions.

Key Feautes:
1) Dual Register Visualization: Real-time updates for both x0-x31 hardware registers and their corresponding ABI names (zero, ra, sp, etc.).

2) Instruction Support: Currently supports 22 core RISC-V instructions, including:
    Arithmetic: add, addi, sub, subi
    Logical shifts: sll, sra, sla
    Control Flow: j, beq, bne, bge, ble
    Data/Pseudo: li, mv, defw, defb

3) Interactive Code Editor: A built-in assembly editor with memory address mapping.
4) Integrated Documentation: A built-in "Command Window" providing a quick-reference guide for RISC-V syntax and meanings.
