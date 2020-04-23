"""CPU functionality."""

import sys
from datetime import datetime 

read_file = sys.argv[1]

# List of instructions

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
INT = 0b01010010
IRET = 0b00010011
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110
LD = 0b10000011
LDI = 0b10000010
MOD = 0b10100100
PRN = 0b01000111
MUL = 0b10100010
NOP = 0b00000000
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PUSH = 0b01000101
RET = 0b00010001
SHL = 0b10101100
SHR = 0b10101101
ST = 0b10000100
SUB = 0b10100001
XOR = 0b10101011

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.IM = 5
        self.IS = 6
        self.sp = 7
        self.fl = 0
        self.reg[self.sp] = 0xF4
        self.running = True
        self.interrupts = True

        # initalizing the branch table to allow O(1) runtime
        self.branchtable = {}
        self.branchtable[ADD] = self.ADD
        self.branchtable[AND] = self.AND
        self.branchtable[CALL] = self.CALL
        self.branchtable[CMP] = self.CMP
        self.branchtable[DEC] = self.DEC
        self.branchtable[DIV] = self.DIV
        self.branchtable[HLT] = self.HLT
        self.branchtable[INC] = self.INC
        self.branchtable[INT] = self.INT
        self.branchtable[IRET] = self.IRET
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JGE] = self.JGE
        self.branchtable[JGT] = self.JGT
        self.branchtable[JLE] = self.JLE
        self.branchtable[JLT] = self.JLT
        self.branchtable[JMP] = self.JMP
        self.branchtable[JMP] = self.JMP
        self.branchtable[LD] = self.LD
        self.branchtable[LDI] = self.LDI
        self.branchtable[MOD] = self.MOD
        self.branchtable[NOP] = self.NOP
        self.branchtable[NOT] = self.NOT
        self.branchtable[OR] = self.OR
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[POP] = self.POP
        self.branchtable[PRA] = self.PRA
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[RET] = self.RET
        self.branchtable[SHL] = self.SHL
        self.branchtable[SHR] = self.SHR
        self.branchtable[ST] = self.ST
        self.branchtable[SUB] = self.SUB
        self.branchtable[XOR] = self.XOR

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(read_file) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                
                if line == '':
                    continue
                
                line = int(line,2)
                # line = bin(line)

                self.ram[address] = line
                # print(self.ram[address])
                address += 1

        # sys.exit()


        # For now, we've just hardcoded a program:
        '''
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        '''

    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] &= 0xFF
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF
        elif op == 'DEC':
            self.reg[reg_a] -= 1
            self.reg[reg_a] &= 0xFF
        elif op == 'INC':
            self.reg[reg_a] += 1
            self.reg[reg_a] &= 0xFF
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF
        elif op == 'CMP':
            val_a = self.reg[reg_a]
            val_b = self.reg[reg_b]
            #`FL` bits: `00000LGE`
            if val_a == val_b:
                self.fl = self.fl | 0b00000001
            else:
                self.fl = self.fl & 0b11111110
            if val_a < val_b:
                self.fl = self.fl | 0b00000100
            else:
                self.fl = self.fl & 0b11111011
            if val_a > val_b:
                self.fl = self.fl | 0b00000010
            else:
                self.fl = self.fl & 0b11111101
        elif op == 'NOT':
            self.reg[reg_a] = ~self.reg[reg_a]
            self.reg[reg_a] &= 0xFF
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
            
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ADD(self):
        # get the register holding first value to be added
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be added
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform the addition
        self.alu('ADD', reg_a, reg_b)

    def AND(self):
        # get the register holding first value to be bitwise-AND
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be bitwise-AND
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform the bitwise-AND
        self.alu('AND', reg_a, reg_b)

    def CALL(self):
        # print('CALL')
        # get pc + 2, the return address
        return_addr = self.pc + 2
        # push the return address to the stack
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], return_addr)
        # set the pc to the value in the given register
        reg_num = self.ram_read(self.pc + 1)
        dest_addr = self.reg[reg_num]

        self.pc = dest_addr

    def CMP(self):
        # get the register holding first value to be compared
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be compared
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU for comparison
        self.alu('CMP', reg_a, reg_b)

    def DEC(self):
        # get the register holding the value to be decremented
        reg_a = self.ram_read(self.pc + 1)
        # use the ALU to preform decrementation
        self.alu('DEC', reg_a, None)

    def DIV(self):
        # get the register holding first value to be divided
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be divided
        reg_b = self.ram_read(self.pc + 2)
        # check to see if the value in reg_b is 0
        if self.reg[reg_b] == 0:
            # if it is 0 print error and halt
            self.running = False
            print('ERROR: Cannot divide by 0')
        else:
            # if not 0 preform division using ALU
            self.alu('DIV', reg_a, reg_b)

    def HLT(self):
        # set running to False so the while loop in run() will exit
        self.running = False

    def INC(self):
        # get register holding the value to be incremented
        reg_a = self.ram_read(self.pc + 1)
        # use ALU to preform incrementation
        self.alu('INC', reg_a, None)

    def INT(self):
        # get register holding interupt value 
        reg_a = self.ram_read(self.pc + 1)
        # set the bit according to the number in reg_a
        self.reg[self.IS] |= 2 ** self.reg[reg_a]
        

    def IRET(self):
        # register R6-R0 are popped of the stack in order
        reg_pos = 6
        while reg_pos >= 0:
            self.reg[reg_pos] = self.ram_read(self.reg[self.sp])
            self.reg[self.sp] += 1
            reg_pos -= 1
        # the FL register is popped off the stack
        self.fl = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        # the return address is popped and stored in PC
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.interrupts = True


    def JEQ(self):
        # check if the equal flag is set
        eql_flg = self.fl & 0b00000001
        if eql_flg:
            # if true, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def JGE(self):
        # check if the equal or greater than flags are set
        eql_flg = self.fl & 0b00000001
        gtr_flg = (self.fl & 0b00000010) >> 1

        if eql_flg or gtr_flg:
            # if true, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def JGT(self):
        # check if the greater than flag is set
        gtr_flg = (self.fl & 0b00000010) >> 1
        if gtr_flg:
            # if true, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def JLE(self):
        # check if the equal or less than flags are set
        eql_flg = self.fl & 0b00000001
        les_flg = (self.fl & 0b00000100) >> 2
        if eql_flg or les_flg:
            # if true, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def JLT(self):
        # check if the less than flag is set
        les_flg = (self.fl & 0b00000100) >> 2
        if les_flg:
            # if true, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def JMP(self):
        # get the register holding the address to jump to
        reg_a = self.ram_read(self.pc + 1)
        # get the destinatnion address that reg_a is holding
        dest_addr = self.reg[reg_a]
        # set PC to dest_addr
        self.pc = dest_addr

    def JNE(self):
        eql_flg = self.fl & 0b00000001
        if not eql_flg:
            # if not True, set PC to address stored in reg_a
            reg_a = self.ram_read(self.pc + 1)
            # get the destinatnion address that reg_a is holding
            dest_addr = self.reg[reg_a]
            # set PC to dest_addr
            self.pc = dest_addr
        else:
            self.pc += 2

    def LD(self):
        # get the register that our value will be stored in
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the memory address that our value is stored in
        reg_b = self.ram_read(self.pc + 2)
        # store our value in reg_a
        self.reg[reg_a] = self.ram_read(self.reg[reg_b])

    def LDI(self):
        # print('LDI')
        # get the register to which the value will be saved
        reg_a = self.ram_read(self.pc + 1)
        # get the value to be saved
        reg_b = self.ram_read(self.pc + 2)
        # save the value to the register
        self.reg[reg_a] = reg_b

    def MOD(self):
        # get the register holding first value to be modulo-d
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be modulo-d
        reg_b = self.ram_read(self.pc + 2)
        # check to see if the value in reg_b is 0
        if self.reg[reg_b] == 0:
            # if it is 0 print error and halt
            self.running = False
            print('ERROR: Cannot divide by 0')
        else:
            # use the ALU to preform modulo
            self.alu('MOD', reg_a, reg_b)

    def MUL(self):
        # get the register holding first value to be multiplied
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be multiplied
        reg_b = self.ram_read(self.pc + 2)
        # preform the multiplication using ALU
        self.alu('MUL', reg_a, reg_b)

    def NOP(self):
        return

    def NOT(self):
        # get the register holding first value to be bitwise-NOT-ed
        reg_a = self.ram_read(self.pc + 1)
        # use ALU to preform bitwise-NOT
        self.alu('NOT', reg_a, None)

    def OR(self):
        # get the register holding first value to be bitwise-OR-ed
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be bitwise-OR-ed
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to prefore bitwise-OR
        self.alu('OR', reg_a, reg_b)

    def POP(self):
        # get the register that our value will be copied to
        reg_a = self.ram_read(self.pc + 1)
        # copy the value in the memory address pointed to by SP into reg_a
        self.reg[reg_a] = self.ram_read(self.reg[self.sp])
        # increment SP
        self.reg[self.sp] += 1

    def PRA(self):
        # print('PRA')
        # get the register holding the value to be printed
        reg_a = self.ram_read(self.pc + 1)
        # get the value to be printed
        pra_num = self.reg[reg_a]
        # change and print the value
        print(chr(pra_num))

    def PRN(self):
        # print('PRN')
        # get the register holding the value to be printed
        reg_a = self.ram_read(self.pc + 1)
        # get the value to be printed
        reg_b = self.reg[reg_a]
        # print the value in decimal
        print(int(reg_b))

    def PUSH(self):
        # decrement SP
        self.reg[self.sp] -= 1
        # get the register holding the value to be copied
        reg_a = self.ram_read(self.pc + 1)
        # write the value in reg_a to the memory address pointed to by SP
        self.ram_write(self.reg[self.sp], self.reg[reg_a])

    def RET(self):
        # print('RET')
        # pop return address from stop of stack
        return_addr = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        # set PC to return address
        self.pc = return_addr

    def SHL(self):
        # get the register holding the value to be shifted left
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the amount we shift the above value left
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform shift left
        self.alu('SHL', reg_a, reg_b)

    def SHR(self):
        # get the register holding the value to be shifted right
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the amount we shift the above value right
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform shift right
        self.alu('SHR', reg_a, reg_b)

    def ST(self):
        # get the register holding the memory address to be written to
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the value we will be writing
        reg_b = self.ram_read(self.pc + 2)
        # write the value in reg_b to the memory address in reg_a
        self.ram_write(self.reg[reg_a], self.reg[reg_b])

    def SUB(self):
        # get the register holding first value to be subtracted
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be subtracted
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform subtraction
        self.alu('SUB', reg_a, reg_b)

    def XOR(self):
        # get the register holding first value to be bitwise-XOR-ed
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be bitwise-XOR-ed
        reg_b = self.ram_read(self.pc + 2)
        # use the ALU to preform bitwise-XOR
        self.alu('XOR', reg_a, reg_b)

    def run(self):
        """Run the CPU."""

        last_time = datetime.now()
        
        # continue to run until a HLT instruction is accessed
        while self.running:

            # self.trace() # <--- Use for debugging

            # check time
            cur_time = datetime.now()
            time_dif = cur_time - last_time
            # print(time_dif)

            # if time is greater than 1 sec, set bit 0 of R6 (IS)
            if time_dif.seconds >= 1:
                self.reg[self.IS] |= 0b00000001
                last_time = cur_time


            if self.interrupts:
                # mask IM and IS
                maskedInterrupts = self.reg[self.IM] & self.reg[self.IS]
                # check each bit if it is set
                bit_pos = 0
                while maskedInterrupts > 0:
                    if maskedInterrupts & 0b00000001:
                        # if the bit is set
                        # disable further interrupts
                        self.interrupts = False
                        # clear the bit in the IS register (R6)
                        self.reg[self.IS] -= 2 ** bit_pos
                        # Push the PC register to the stack
                        self.reg[self.sp] -= 1
                        self.ram_write(self.reg[self.sp], self.pc)
                        # push the FL register to the stack
                        self.reg[self.sp] -= 1
                        self.ram_write(self.reg[self.sp], self.fl)
                        # registers R0-R6 are pushed to the stack in that order
                        reg_num = 0
                        while reg_num <= 6:
                            # print(reg_num)
                            # print(self.reg[self.sp])
                            self.reg[self.sp] -= 1
                            self.ram_write(self.reg[self.sp], self.reg[reg_num])
                            reg_num += 1
                        # the address of the appropriate handler is looked up from the interrupt table
                        int_hdl = self.ram_read(0xf8 + bit_pos)
                        # the pc is set to the handler address
                        self.pc = int_hdl
                        break
                    else:
                        bit_pos += 1
                        maskedInterrupts >>= 1

            # get the next instruction from memory
            self.ir = self.ram_read(self.pc)
            
            # determine the amount of memory locations after that will be used
            inst_len = ((self.ir & 0b11000000) >> 6) + 1

            # check auto-increment
            auto_inc = ((self.ir & 0b00010000) >> 4)

            # preform the instruction
            self.branchtable[self.ir]()

            # check if auto_inc == False
            if not auto_inc:
                # increment the PC
                self.pc += inst_len
