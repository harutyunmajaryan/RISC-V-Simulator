
class BennettFunctionality:
        def __init__(self,table_abi=None, table_rv32=None):
            self.registers = {f"x{i}": 0 for i in range(32)}
            self.pc = 0
            self.register_mapping = ["ra","sp","zero","t0","t1","t2","t3","t4","t5","t6","s0","s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","a0","a1","a2","a3","a4","a5","a6","a7",
                                     "x0","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","x21","x22","x23","x24","x25","x26","x27","x28","x29","x30","x31"]
            self.table_abi = table_abi
            self.table_rv32 = table_rv32


#######################assign function##############################
        def assign(self, line):
            line = line.split(";")[0].strip()
            if not line:
                return None

            line = line.replace("(", " ").replace(")", " ")
            parts = line.split()

            if len(parts) != 3:
                return None

            keyword = parts[1]

            if keyword in ["defw", "defb"]:
              if keyword == "defw" and parts[2].isdigit():
                try:
                    return {
                        "opcode": keyword,
                        "name": parts[0],
                        "value": int(parts[2]),
                    }

                except (IndexError, ValueError):
                    return None


              elif keyword == "defb" and not parts[2].isdigit():
                  try:
                      return {
                          "opcode": keyword,
                          "name": parts[0],
                          "string": str(parts[2]),
                      }
                  except (IndexError, ValueError):
                      return None

            return None
#############################################################################


#######################loading instructions##################################
        def loading_instruction1(self, line):
            line = line.split(";")[0].strip()

            if not line:
                return None

            if line.count(",") != 1:
                return None

            line = line.replace(",", " ")
            parts = line.split()
            

            if len(parts) == 3 and parts[0] == "li":
                target_reg = parts[1]
                if target_reg not in self.register_mapping:
                    return None

                try:
                    imm = int(parts[2])
                    hex_val = f"{imm & 0xFFFFFFFF:08X}"

                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == target_reg:
                            if target_reg == "x0":
                                self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                  self.table_rv32.item(row_id, values=(target_reg, hex_val, "...."))
                            break

                    for row_id in self.table_abi.get_children():
                        if self.table_abi.item(row_id)['values'][0] == target_reg:
                            if target_reg == "zero":
                                self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                self.table_abi.item(row_id, values=(target_reg, hex_val, "...."))
                            break

                    return {"opcode": "li", "destination register": target_reg, "imm": imm}


                except (IndexError, ValueError):
                    return None
            return None






#############################################################################

#######################arithmetic instruction function###################################

        def arithmetic_instructions(self, line):
            line = line.split(";")[0].strip()
            if not line:
                return None

            if line.count(",") != 2:
                return None

            line = line.replace(",", " ")
            parts = line.split()

            if len(parts) != 4:
                return None

            keyword = parts[0]

            if keyword not in ["addi", "subi", "add", "sub"]:
                return None

            if keyword == "addi" and len(parts) == 4:
                target_reg = parts[1]
                if target_reg not in self.register_mapping:
                    return None

                try:
                    imm = int(parts[3])
                    source_register = parts[2]

                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == target_reg:
                            if target_reg == "x0":
                                self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_rv32.get_children():
                                    if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result  = value_in_source_reg + imm
                                        result_in_hex =  f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    for row_id in self.table_abi.get_children():
                        if self.table_abi.item(row_id)['values'][0] == target_reg:
                            if target_reg == "zero":
                                self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_abi.get_children():
                                    if self.table_abi.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result  = value_in_source_reg + imm
                                        result_in_hex =  f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_abi.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    return {"opcode": "addi", "destination register": target_reg,"source register": source_register, "imm": imm}

                except ValueError:
                    return None

            elif keyword == "subi" and len(parts) == 4:
                    target_reg = parts[1]
                    if target_reg not in self.register_mapping:
                        return None

                    try:
                        imm = int(parts[3])
                        source_register = parts[2]

                        for row_id in self.table_rv32.get_children():
                            if self.table_rv32.item(row_id)['values'][0] == target_reg:
                                if target_reg == "x0":
                                    self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_rv32.get_children():
                                        if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                            value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_in_source_reg, 16)
                                            result = value_in_source_reg - imm
                                            result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                            self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                                break

                        for row_id in self.table_abi.get_children():
                            if self.table_abi.item(row_id)['values'][0] == target_reg:
                                if target_reg == "zero":
                                    self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_abi.get_children():
                                        if self.table_abi.item(row_id2)['values'][0] == source_register:
                                            value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_in_source_reg, 16)
                                            result = value_in_source_reg - imm
                                            result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                            self.table_abi.item(row_id, values=(target_reg, result_in_hex, "...."))
                                break

                        return {"opcode": "subi", "destination register": target_reg, "source register": source_register, "imm": imm}

                    except ValueError:
                        return None

            elif keyword == "add" and len(parts) == 4:
                    target_reg = parts[1]
                    if target_reg not in self.register_mapping:
                        return None

                    try:
                        source_register_2 = parts[3]
                        source_register = parts[2]

                        for row_id in self.table_rv32.get_children():
                            if self.table_rv32.item(row_id)['values'][0] == target_reg:
                                if target_reg == "x0":
                                    self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_rv32.get_children():
                                        if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                                 value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                                 value_in_source_reg = int(value_in_source_reg, 16)
                                                 for row_id3 in self.table_rv32.get_children():
                                                    if self.table_rv32.item(row_id3)['values'][0] == source_register_2:
                                                      value_in_source_reg_2 = str(self.table_rv32.item(row_id3)['values'][1])
                                                      value_in_source_reg_2 = int(value_in_source_reg_2, 16)
                                                      result = value_in_source_reg + value_in_source_reg_2
                                                      result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                                      self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                                break

                        for row_id in self.table_abi.get_children():
                            if self.table_abi.item(row_id)['values'][0] == target_reg:
                                if target_reg == "zero":
                                    self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_abi.get_children():
                                        if self.table_abi.item(row_id2)['values'][0] == source_register:
                                            value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_in_source_reg, 16)
                                            for row_id3 in self.table_abi.get_children():
                                                if self.table_abi.item(row_id3)['values'][0] == source_register_2:
                                                    value_in_source_reg_2 = str(self.table_abi.item(row_id3)['values'][1])
                                                    value_in_source_reg_2 = int(value_in_source_reg_2, 16)
                                                    result = value_in_source_reg + value_in_source_reg_2
                                                    result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                                    self.table_abi.item(row_id,
                                                                         values=(target_reg, result_in_hex, "...."))
                                break

                        return {"opcode": "add", "destination register": target_reg, "source register": source_register, "2nd source register": source_register_2}

                    except ValueError:
                        return None


            elif keyword == "sub" and len(parts) == 4:
                    target_reg = parts[1]
                    if target_reg not in self.register_mapping:
                        return None

                    try:
                        source_register_2 = parts[3]
                        source_register = parts[2]

                        for row_id in self.table_rv32.get_children():
                            if self.table_rv32.item(row_id)['values'][0] == target_reg:
                                if target_reg == "x0":
                                    self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_rv32.get_children():
                                        if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                                 value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                                 value_in_source_reg = int(value_in_source_reg, 16)
                                                 for row_id3 in self.table_rv32.get_children():
                                                    if self.table_rv32.item(row_id3)['values'][0] == source_register_2:
                                                      value_in_source_reg_2 = str(self.table_rv32.item(row_id3)['values'][1])
                                                      value_in_source_reg_2 = int(value_in_source_reg_2, 16)
                                                      result = value_in_source_reg - value_in_source_reg_2
                                                      result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                                      self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                                break

                        for row_id in self.table_abi.get_children():
                            if self.table_abi.item(row_id)['values'][0] == target_reg:
                                if target_reg == "zero":
                                    self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                                else:
                                    for row_id2 in self.table_abi.get_children():
                                        if self.table_abi.item(row_id2)['values'][0] == source_register:
                                            value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_in_source_reg, 16)
                                            for row_id3 in self.table_abi.get_children():
                                                if self.table_abi.item(row_id3)['values'][0] == source_register_2:
                                                    value_in_source_reg_2 = str(self.table_abi.item(row_id3)['values'][1])
                                                    value_in_source_reg_2 = int(value_in_source_reg_2, 16)
                                                    result = value_in_source_reg - value_in_source_reg_2
                                                    result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                                    self.table_abi.item(row_id,
                                                                         values=(target_reg, result_in_hex, "...."))
                                break

                        return {"opcode": "sub", "destination register": target_reg, "source register": source_register, "2nd source register": source_register_2}

                    except ValueError:
                        return None



###################jump branch################################
        def j_branch(self, line, all_lines):
            line = line.split(";")[0].strip()
            if not line:
                return None

            parts = line.split()
            if len(parts) != 2:
                return None

            if line.count(",") != 0:
                return None

            keyword = parts[0]
            if keyword != "j":
                return None
            else:
                try:
                    label = parts[1]
                    for index, code_line in enumerate(all_lines):
                        clean_line = code_line.split(";")[0].strip()
                        if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                break

                    return {
                        "keyword": keyword,
                        "label": label,
                    }

                except (IndexError, ValueError):
                    return None

#############################################################


########################Shifts###############################
        def shifted_operations(self,line):
            line = line.split(";")[0].strip()
            if not line:
                return None

            if line.count(",") != 2:
                return None

            line = line.replace(",", " ")
            parts = line.split()

            if len(parts) != 4:
                return None

            keyword = parts[0]

            if keyword not in ["sll","sla","sra"]:
                return None

            if keyword == "sll" and len(parts) == 4:
                target_reg = parts[1]
                if target_reg not in self.register_mapping:
                    return None
                try:
                    source_register = parts[2]
                    imm = int(parts[3])

                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == target_reg:
                            if target_reg == "x0":
                                self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_rv32.get_children():
                                    if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg * pow(2,imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    for row_id in self.table_abi.get_children():
                        if self.table_abi.item(row_id)['values'][0] == target_reg:
                            if target_reg == "zero":
                                self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_abi.get_children():
                                    if self.table_abi.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg * pow(2,imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_abi.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    return {"opcode": keyword, "destination register": target_reg, "source register": source_register, "immediate(shifts)": imm}

                except (ValueError,IndexError):
                    return None


            elif keyword == "sla" and len(parts) == 4:
                target_reg = parts[1]
                if target_reg not in self.register_mapping:
                    return None
                try:
                    source_register = parts[2]
                    imm = int(parts[3])

                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == target_reg:
                            if target_reg == "x0":
                                self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_rv32.get_children():
                                    if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg * pow(2, imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    for row_id in self.table_abi.get_children():
                        if self.table_abi.item(row_id)['values'][0] == target_reg:
                            if target_reg == "zero":
                                self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_abi.get_children():
                                    if self.table_abi.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg * pow(2,imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_abi.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    return {"opcode": keyword, "destination register": target_reg, "source register": source_register, "immediate(shifts)": imm}

                except (ValueError, IndexError):
                    return None


            elif keyword == "sra" and len(parts) == 4:
                target_reg = parts[1]
                if target_reg not in self.register_mapping:
                    return None
                try:
                    source_register = parts[2]
                    imm = int(parts[3])

                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == target_reg:
                            if target_reg == "x0":
                                self.table_rv32.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_rv32.get_children():
                                    if self.table_rv32.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_rv32.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg // pow(2, imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_rv32.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    for row_id in self.table_abi.get_children():
                        if self.table_abi.item(row_id)['values'][0] == target_reg:
                            if target_reg == "zero":
                                self.table_abi.item(row_id, values=(target_reg, "00000000", "...."))
                            else:
                                for row_id2 in self.table_abi.get_children():
                                    if self.table_abi.item(row_id2)['values'][0] == source_register:
                                        value_in_source_reg = str(self.table_abi.item(row_id2)['values'][1])
                                        value_in_source_reg = int(value_in_source_reg, 16)
                                        result = value_in_source_reg // pow(2,imm)
                                        result_in_hex = f"{(result & 0xFFFFFFFF):08X}"
                                        self.table_abi.item(row_id, values=(target_reg, result_in_hex, "...."))
                            break

                    return {"opcode": keyword, "destination register": target_reg, "source register": source_register, "immediate(shifts)": imm}

                except (ValueError, IndexError):
                    return None

#################################################################



######################conditions##################################
        def conditional_non_zero_branch(self, line, all_lines):
            line = line.split(";")[0].strip()
            if not line:
                return None

            if line.count(",") != 2:
                return None

            line = line.replace(",", " ")
            parts = line.split()

            if len(parts) != 4:
                return None

            keyword = parts[0]
            if keyword not in ["bne","bge","ble","beq"]:
                return None


            should_jump = False
            if keyword == "beq" and len(parts) == 4:
                try:
                    register1 = parts[1]
                    register2 = parts[2]
                    label = parts[3]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            for row_id2 in self.table_rv32.get_children():
                                if self.table_rv32.item(row_id2)['values'][0] == register2:
                                    value_in_register2 = str(self.table_rv32.item(row_id2)['values'][1])
                                    value_in_register2_hex = int(value_in_register2, 16)
                                    if value_in_register1_hex == value_in_register2_hex:
                                        should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError,IndexError):
                    return None

            elif keyword == "bne" and len(parts) == 4:
                try:
                    register1 = parts[1]
                    register2 = parts[2]
                    label = parts[3]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            for row_id2 in self.table_rv32.get_children():
                                if self.table_rv32.item(row_id2)['values'][0] == register2:
                                    value_in_register2 = str(self.table_rv32.item(row_id2)['values'][1])
                                    value_in_register2_hex = int(value_in_register2, 16)
                                    if value_in_register1_hex != value_in_register2_hex:
                                        should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None


            elif keyword == "ble" and len(parts) == 4:
                try:
                    register1 = parts[1]
                    register2 = parts[2]
                    label = parts[3]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            for row_id2 in self.table_rv32.get_children():
                                if self.table_rv32.item(row_id2)['values'][0] == register2:
                                    value_in_register2 = str(self.table_rv32.item(row_id2)['values'][1])
                                    value_in_register2_hex = int(value_in_register2, 16)
                                    if value_in_register1_hex <= value_in_register2_hex:
                                        should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None

            elif keyword == "bge" and len(parts) == 4:
                try:
                    register1 = parts[1]
                    register2 = parts[2]
                    label = parts[3]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            for row_id2 in self.table_rv32.get_children():
                                if self.table_rv32.item(row_id2)['values'][0] == register2:
                                    value_in_register2 = str(self.table_rv32.item(row_id2)['values'][1])
                                    value_in_register2_hex = int(value_in_register2, 16)
                                    if value_in_register1_hex >= value_in_register2_hex:
                                        should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None

#########################################################################

#########################################################################
        def conditional_zero_branch(self,line,all_lines):
            line = line.split(";")[0].strip()
            if not line:
                return None

            if line.count(",") != 1:
                return None

            line = line.replace(",", " ")
            parts = line.split()

            if len(parts) != 3:
                return None

            keyword = parts[0]
            if keyword not in ["bnez","bgez","beqz","blez"]:
                return None

            should_jump = False

            if keyword == "beqz" and len(parts) == 3:
                try:
                    register1 = parts[1]
                    label = parts[2]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            if value_in_register1_hex == 0:
                                    should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None

            elif keyword == "bnez" and len(parts) == 3:
                try:
                    register1 = parts[1]
                    label = parts[2]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            if value_in_register1_hex != 0:
                                    should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None


            elif keyword == "blez" and len(parts) == 3:
                try:
                    register1 = parts[1]
                    label = parts[2]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            if value_in_register1_hex <= 0:
                                    should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None

            elif keyword == "bgez" and len(parts) == 3:
                try:
                    register1 = parts[1]
                    label = parts[2]
                    for row_id in self.table_rv32.get_children():
                        if self.table_rv32.item(row_id)['values'][0] == register1:
                            value_in_register1 = str(self.table_rv32.item(row_id)['values'][1])
                            value_in_register1_hex = int(value_in_register1, 16)
                            if value_in_register1_hex >= 0:
                                    should_jump = True

                    if should_jump:
                        for index, code_line in enumerate(all_lines):
                            clean_line = code_line.split(";")[0].strip()
                            if clean_line == f"{label}:" or clean_line == f"{label}":
                                self.pc = index
                                return True
                    return False

                except (ValueError, IndexError):
                    return None

########################mv instruction function########################################################
        def mv_instruction(self,line):
            line = line.split(";")[0].strip()
            if not line:
                return None

            if line.count(",") != 1:
                return None

            line = line.replace(",", " ")
            parts = line.split()

            if len(parts) != 3:
                return None

            keyword = parts[0]
            if keyword == "mv" and len(parts) == 3:
                try:
                    destination_register = parts[1]
                    source_register = parts[2]

                    for row_id in self.table_rv32.get_children():
                        if (self.table_rv32.item(row_id)['values'][0] == destination_register) and (destination_register in self.register_mapping):
                            if destination_register == "x0":
                                self.table_rv32.item(row_id, values=(destination_register, "00000000", "...."))
                            else:
                                for row_id2 in self.table_rv32.get_children():
                                    if (self.table_rv32.item(row_id2)['values'][0] == source_register) and (source_register in self.register_mapping):
                                            value_source_string = str(self.table_rv32.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_source_string, 16)
                                            hex_val_in_destination_register = f"{value_in_source_reg & 0xFFFFFFFF:08X}"
                                            self.table_rv32.item(row_id, values = (destination_register, hex_val_in_destination_register, "...."))

                            return {"opcode": keyword, "destination register": destination_register, "source register": source_register}



                    for row_id in self.table_abi.get_children():
                        if (self.table_abi.item(row_id)['values'][0] == destination_register) and (destination_register in self.register_mapping):
                            if destination_register == "zero":
                                self.table_abi.item(row_id, values=(destination_register, "00000000", "...."))
                            else:
                                for row_id2 in self.table_abi.get_children():
                                    if (self.table_abi.item(row_id2)['values'][0] == source_register) and (source_register in self.register_mapping):
                                            value_source_string = str(self.table_abi.item(row_id2)['values'][1])
                                            value_in_source_reg = int(value_source_string, 16)
                                            hex_val_in_destination_register = f"{value_in_source_reg & 0xFFFFFFFF:08X}"
                                            self.table_abi.item(row_id, values = (destination_register, hex_val_in_destination_register, "...."))

                            return {"opcode": keyword, "destination register": destination_register, "source register": source_register}


                except (ValueError, IndexError):
                    return None



#######################################################################################################################

