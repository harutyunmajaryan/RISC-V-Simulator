# Bennett

A lightweight, visual RISC-V assembly simulator built with Python and Tkinter.

Bennett helps students and developers see how the CPU state changes in real time as instructions are executed. Unlike traditional command-line simulators, it shows registers in a dual view (hardware names and ABI names) to help users master RISC-V calling conventions.

## Key features

1. **Dual register visualization:** real-time updates for both the `x0`-`x31` hardware registers and their corresponding ABI names (`zero`, `ra`, `sp`, etc.).
2. **Instruction support:** currently supports 25 core RISC-V instructions, including those in the table below.
3. **Interactive code editor:** a built-in assembly editor with memory address mapping.
4. **Integrated documentation:** a built-in "Command Window" with a quick-reference guide to RISC-V syntax and meanings.

### Supported instructions

| Category | Instructions |
|---|---|
| Arithmetic | `add`, `addi`, `sub`, `subi`, `mul`, `muli` |
| Logical shifts | `sll`, `sra`, `sla` |
| Control flow | `j`, `beq`, `bne`, `bge`, `ble` |
| Data / pseudo | `li`, `mv`, `defw`, `defb` |

## Tech stack

- **Language:** Python
- **GUI:** Tkinter

## Getting started

**Prerequisites:** Python 3 (Tkinter is included with most Python installations).

```bash
git clone https://github.com/harutyunmajaryan/RISC-V-Simulator.git
cd RISC-V-Simulator
python3 CPU.py
```

## Future improvements

- [ ] **Memory implementation:** add a Data Memory (RAM) table for `lw` and `sw` instructions.
- [ ] **Step execution:** add a "Step" button to execute code one line at a time for easier debugging.
- [ ] **Console output:** implement an `ecall` system to print results to a virtual console.
