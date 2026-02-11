import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import os
from Bennett_functionality import *


class BennettWindow:
    def __init__(self):
        ##################1st layer#################################
        self.main_window = tk.Tk()
        self.main_window_label = tk.Label(
            self.main_window,
            text="Bennett RISC-V Emulator",
            fg="gray",
            bg="white"
        )
        self.main_window_label.grid(row=0, column=0, columnspan=2, pady=2, padx=350)

        self.main_window.title("Bennett RISC-V Emulator")
        self.main_window.geometry("800x595")
        self.main_window.resizable(False, False)
        self.main_window.configure(background="white")

        self.button_frame = tk.Frame(self.main_window, bg="white", padx=1)
        self.button_frame.grid(row=1, column=0, columnspan=4, sticky="w", padx=0)

        # ------------------- TOP MENU BUTTONS -------------------
        self.button_file = tk.Button(
            self.button_frame,
            text="File",
            bg="white",
            fg="black",
            width=6,
            command=self.open_file_menu
        )
        self.button_file.grid(row=0, column=0, padx=0, pady=0)

        self.button_support = tk.Button(
            self.button_frame,
            text="Support",
            bg="white",
            fg="black",
            width=6,
            command = self.open_support_menu
        )
        self.button_support.grid(row=0, column=1, padx=0, pady=0)

        self.button_windows = tk.Button(
            self.button_frame,
            text="Windows",
            bg="white",
            fg="black",
            width=7,
            command = self.open_window_menu
        )
        self.button_windows.grid(row=0, column=2, padx=0, pady=0)

        self.button_asm = tk.Button(
            self.button_frame,
            text="Compile",
            bg="white",
            fg="black",
            width=17,
            command = self.open_assembly_menu
        )
        self.button_asm.grid(row=0, column=3, padx=0, pady=0)
        # ----------------------------------------------------------

        self.file_menu = tk.Menu(self.main_window, tearoff=0)
        self.file_menu.add_command(label="Open",command=self.open_file)


        self.support_menu = tk.Menu(self.main_window, tearoff=0)
        self.support_menu.add_command(label="Where to code",command = self.where_to_code)
        self.support_menu.add_command(label="How to code", command = self.how_to_code)

        self.window_menu = tk.Menu(self.main_window, tearoff=0)
        self.window_menu.add_command(label="Terminal Window")
        self.window_menu.add_command(label="Command Window", command = self.command_window)

        self.asm_menu = tk.Menu(self.main_window, tearoff=0)
        self.asm_menu.add_command(label="Assemble File")


        ###############2nd layer: horizontal frame for buttons ########################
        self.button_frame2 = tk.Frame(
            self.main_window,
            bg="white",
            relief="solid",
            bd=0.5,
            width=320,
            height=508
        )
        self.button_frame2.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
        self.button_frame2.grid_propagate(False)


        self.button_run = tk.Button(
            self.button_frame2,
            text="Run",
            bg="white",
            fg="black",
            width=8,
            height=2,
            command = self.run_simulation
        )
        self.button_run.grid(row=0, column=0)

        self.button_stop = tk.Button(
            self.button_frame2,
            text="Stop",
            bg="white",
            fg="black",
            width=8,
            height=2
        )
        self.button_stop.grid(row=0, column=1)

        self.button_reset = tk.Button(
            self.button_frame2,
            text="Reset",
            bg="white",
            fg="black",
            width=8,
            height=2
        )
        self.button_reset.grid(row=0, column=2)
        ##################################################

        ################3rd frame inside 2nd frame########
        self.button_frame3 = tk.Frame(
            self.main_window,
            bg="white",
            relief="solid",
            bd=0.5,
            width=320,
            height=400
        )
        self.button_frame3.grid(row=2, column=0, sticky="nw", padx=10, pady=50)
        self.button_frame3.grid_propagate(False)

        self.button_frame4 = tk.Frame(
            self.main_window,
            bg="white",
            relief="solid",
            bd=0.5,
            width=320,
            height=400
        )
        self.button_frame4.grid(row=2, column=0, sticky="nw", padx=10, pady=290)
        self.button_frame4.grid_propagate(False)
        ##################################################


        ##################table for registers###########################
        columns = ("Register(ABI)", "Value", "ASCII")
        self.table_ABI = ttk.Treeview(self.button_frame3, columns=columns, show="headings")


        for col in columns:
            self.table_ABI.heading(col, text=col)
            self.table_ABI.column(col, width=100, anchor="center")


        data = [
            ("PC","00000000", "...."),
            ("ra", "00000000", "...."),
            ("sp", "00000000", "...."),
            ("zero", "00000000", "...."),
            ("t0", "00000000", "...."),
            ("t1", "00000000", "...."),
            ("t2", "00000000", "...."),
            ("t3", "00000000", "...."),
            ("t4", "00000000", "...."),
            ("t5", "00000000", "...."),
            ("t6", "00000000", "...."),
            ("s0", "00000000", "...."),
            ("s1", "00000000", "...."),
            ("s2", "00000000", "...."),
            ("s3", "00000000", "...."),
            ("s4", "00000000", "...."),
            ("s5", "00000000", "...."),
            ("s6", "00000000", "...."),
            ("s7", "00000000", "...."),
            ("s8", "00000000", "...."),
            ("s9", "00000000", "...."),
            ("s10", "00000000", "...."),
            ("s11", "00000000", "...."),
            ("a0", "00000000", "...."),
            ("a1", "00000000", "...."),
            ("a2", "00000000", "...."),
            ("a3", "00000000", "...."),
            ("a4", "00000000", "...."),
            ("a5", "00000000", "...."),
            ("a6", "00000000", "...."),
            ("a7", "00000000", "...."),

        ]

        for row in data:
            self.table_ABI.insert("", tk.END, values=row)


        scrollbar = ttk.Scrollbar(self.button_frame3, orient="vertical", command=self.table_ABI.yview, )
        self.table_ABI.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.table_ABI.pack(side="left", fill="both", expand=True)


        #2nd table
        columns = ("Register(RV32)", "Value", "ASCII")
        self.table_RV32 = ttk.Treeview(self.button_frame4, columns=columns, show="headings")


        for col in columns:
            self.table_RV32.heading(col, text=col)
            self.table_RV32.column(col, width=100, anchor="center")


        data = [
            ("x0", "00000000", "...."),
            ("x1", "00000000", "...."),
            ("x2", "00000000", "...."),
            ("x3", "00000000", "...."),
            ("x4", "00000000", "...."),
            ("x5", "00000000", "...."),
            ("x6", "00000000", "...."),
            ("x7", "00000000", "...."),
            ("x8", "00000000", "...."),
            ("x9", "00000000", "...."),
            ("x10", "00000000", "...."),
            ("x11", "00000000", "...."),
            ("x12", "00000000", "...."),
            ("x13", "00000000", "...."),
            ("x14", "00000000", "...."),
            ("x15", "00000000", "...."),
            ("x16", "00000000", "...."),
            ("x17", "00000000", "...."),
            ("x18", "00000000", "...."),
            ("x19", "00000000", "...."),
            ("x20", "00000000", "...."),
            ("x21", "00000000", "...."),
            ("x22", "00000000", "...."),
            ("x23", "00000000", "...."),
            ("x24", "00000000", "...."),
            ("x25", "00000000", "...."),
            ("x26", "00000000", "...."),
            ("x27", "00000000", "...."),
            ("x28", "00000000", "...."),
            ("x29", "00000000", "...."),
            ("x30", "00000000", "...."),
            ("x31", "00000000", "...."),
            ("PC", "00000000", "...."),

        ]

        for row in data:
            self.table_RV32.insert("", tk.END, values=row)

        scrollbar = ttk.Scrollbar(self.button_frame4, orient="vertical", command=self.table_RV32.yview, )
        self.table_RV32.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.table_RV32.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")
        self.table_RV32.pack(side="left", fill="both", expand=True)
        #####################################################

        ###############code window########################
        self.code_frame = tk.Frame(
            self.main_window,
            bg="#f0f0f0",
            bd=2,
            relief="solid",
            width=460,
            height=560
        )
        self.code_frame.place(x=340, y=61)
        self.code_frame.grid_propagate(False)

        for i in range(30):
            addr = f"{i * 4:08X}"
            btn = tk.Button(self.code_frame, text=addr, font=('Arial', 10), bg="#f0f0f0", fg="black", width=12)
            btn.place(x=0, y=i * 25)

        self.code_content = tk.Text(self.code_frame, bg="#f0f0f0", fg="black")
        self.code_content.place(x=100, y=0, width=360, height=550)
        ###################################################


    def open_file_menu(self):
        x = self.button_file.winfo_rootx()
        y = self.button_file.winfo_rooty() + self.button_file.winfo_height()
        self.file_menu.post(x, y)

    def open_support_menu(self):
        x = self.button_support.winfo_rootx()
        y = self.button_support.winfo_rooty() + self.button_support.winfo_height()
        self.support_menu.post(x, y)

    def open_window_menu(self):
        x = self.button_windows.winfo_rootx()
        y = self.button_windows.winfo_rooty() + self.button_windows.winfo_height()
        self.window_menu.post(x, y)

    def open_assembly_menu(self):
        x = self.button_asm.winfo_rootx()
        y = self.button_asm.winfo_rooty() + self.button_asm.winfo_height()
        self.asm_menu.post(x, y)

    ###############buttons functionality##############


    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Files",
            filetypes=[("All Files", "*.*")]
        )
        if file_path.endswith(".s"):
            with open(file_path, "r") as file:
               file_content = file.read()
               self.code_content.insert("1.0", file_content)
            return file_content
        else:
            messagebox.showerror("Error", "Please select valid assembly file")
            pass

        if not file_path:
            return



    def save_file(self):
        desktop = os.path.join(os.path.expanduser("~"), "All Files")

        file_path = filedialog.asksaveasfilename(
            defaultextension=".s",
            initialdir=desktop,
            title="Save Assembly File",
            filetypes=[(".s", "*.s")]
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write("your content here")



    def where_to_code(self):
        guide_window = tk.Toplevel(self.main_window,bg="white")
        guide_window.title("Guidelines")
        guide_window.geometry("450x150")
        guide_window_text = tk.Label(
            guide_window,
            text=("Before opening a file, create your assembly code locally or on Linux and save it "
        "with a .s extension. Make sure the file is saved properly before opening and uploading it. "
        "To upload the file, navigate to File → Open, and select your .s file. "
        "Once opened, your code will appear on the right side of the window. Click Run to execute the simulator."),
            bg="white",
            fg="black",
            font=('Arial', 10),
            wraplength=400,
            justify="left"
        )
        guide_window_text.place(x=10, y=10)

    def how_to_code(self):
        how_to_code_window = tk.Toplevel(self.main_window,bg="white")
        how_to_code_window.title("Guidelines")
        how_to_code_window.geometry("450x150")
        how_to_code_text = tk.Label(how_to_code_window,
        text = ("To start coding, visit RISC-Vise website that provides tutorials, "
        "documentation, and example projects relevant to your programming language or assignment. Explore the webpage "
        "to understand coding concepts, syntax, and best practices. Try out the coding examples on your "
        "own system to reinforce your learning. Gradually, apply these concepts to create your own programs and "
        "experiments."
        ),
        bg="white",
        fg="black",
        font=('Arial', 10),
        wraplength=400,
        justify="left"
        )
        how_to_code_text.place(x=10, y=10)


    def command_window(self):
            command_table = tk.Toplevel(self.main_window)
            command_table.title("RISC-V Assembly Commands")
            command_table.geometry("1000x400-170-2")

            columns = ("Category", "Instruction", "Example", "Meaning")


            tree = ttk.Treeview(command_table, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            for col in columns:
                tree.heading(col, text=col)

            tree.column("Category", width=180, minwidth=160, anchor="center")
            tree.column("Instruction", width=100, minwidth=90, anchor="center")
            tree.column("Example", width=280, minwidth=240, anchor="center")
            tree.column("Meaning", width=320, minwidth=260, anchor="center")

            tree.insert("", "end", values=("Arithmetic", "add", "add x1, x2, x3", "x1 = x2 + x3"))
            tree.insert("", "end", values=("Arithmetic", "sub", "sub x1, x2, x3", "x1 = x2 - x3"))
            tree.insert("", "end", values=("Arithmetic(Immediate)", "addi", "addi x1, x2, 5", "x1 = x2 + 5"))
            tree.insert("", "end", values=("Arithmetic(Immediate)", "subi", "subi x1, x2, 5", "x1 = x2 - 5"))
            tree.insert("", "end", values=("Data Transfer", "lw", "lw x1, 10[x2]", "x1 -> Memory[x2 + 10]"))
            tree.insert("", "end", values=("Data Transfer", "sw", "sw x1, 0[x2]", "Memory[x2 + 0] -> x1"))
            tree.insert("", "end", values=("Data Transfer", "lb", "lb x1, 0[x2]", "x1 -> Memory[x2 + 0]"))
            tree.insert("", "end", values=("Data Transfer", "sb", "sb x1, 5[x2]", "Memory[x2 + 5] -> x1"))
            tree.insert("", "end", values=("Data Transfer", "li", "li x1, 10", "x1 = 10"))
            tree.insert("", "end", values=("Shift (Left) Logical", "sll", "sll x1, x1, 4", "x1 = x1 * 2^4 (Unsigned)"))
            tree.insert("", "end", values=("Shift (Right) Logical", "srl", "srl x2, x2, 2", "x2 = x2 / 2^2 (Unsigned)"))
            tree.insert("", "end", values=("Shift Arithmetic", "sra", "sra x2, x2, 2", "x2 = x2 / 2^2 (Signed)"))
            tree.insert("", "end", values=("Special Case", "li x17, ...", "li x17, 0–5", "Syscall selector"))
            tree.insert("", "end", values=("Special Case", "ecall", "ecall", "Environment call"))
            tree.insert("", "end", values=("Conditional Jump", "beq", "beq x1, x2, condition", "Condition that checks if x1 and x2 are equal"))
            tree.insert("", "end", values=("Conditional Jump", "bne", "bne x1, x2, condition", "Condition that checks if x1 is not equal to x2"))
            tree.insert("", "end", values=("Conditional Jump", "bge", "bge x1, x2, condition", "Condition that checks if x1 is greater/equal than x2"))
            tree.insert("", "end", values=("Conditional Jump", "blt", "blt x1, x2, condition", "Condition that checks if x1 is less than x2"))
            tree.insert("", "end", values=("Conditional Jump", "blt", "blt x1, x2, condition", "Condition that checks if x1 is less than x2"))
            tree.insert("", "end", values=("Conditional Jump", "bnez", "bnez x1, condition", "Condition that checks if x1 is not equal to 0"))
            tree.insert("", "end", values=("Conditional Jump", "beqz", "beqz x1, condition", "Condition that checks if x1 is equal to 0"))


    ######################ENGINE#####################################
    def run_simulation(self):
        text_data = self.code_content.get("1.0", "end-1c")
        lines = text_data.splitlines()
        engine = BennettFunctionality(table_abi=self.table_ABI, table_rv32=self.table_RV32)


        engine.pc = 0
        while engine.pc < len(lines):
            single_line = lines[engine.pc]
            line = single_line.split(";")[0].strip()

            if not line or line.endswith(":"):
                engine.pc += 1
                continue

            parts = line.replace(",", " ").split()
            opcode = parts[0].lower()

            result = None

            if opcode == "li":
                result = engine.loading_instruction1(line)

            elif opcode in ["add", "sub", "addi", "subi"]:
                result = engine.arithmetic_instructions(line)

            elif opcode == "j":
                result = engine.j_branch(line, all_lines=lines)
                if result:
                    print(f"Jump Executed: {result}")
                    continue

            elif opcode in ["beq", "bge", "bne", "ble"]:
                result = engine.conditional_non_zero_branch(line,all_lines=lines)
                if result is True:
                    continue

                if result is False:
                    result = "handled"

            elif opcode in ["beqz", "bgez", "bnez", "blez"]:
                result = engine.conditional_zero_branch(line, all_lines=lines)
                if result is True:
                    continue

                if result is False:
                    result = "handled"


            elif opcode in ["sll","sla","sra"]:
                result = engine.shifted_operations(line)

            elif opcode in ["defw", "defb"]:
                result = engine.assign(line)

            elif opcode == "mv":
                result = engine.mv_instruction(line)


            if result:
                print(f"Executed: {result}")
            else:
                messagebox.showerror("Error", f"Unrecognized instruction: {line}")
                break

            engine.pc += 1

    ######################################################################################################





    def run(self):
        self.main_window.mainloop()


run = BennettWindow()
run.run()
