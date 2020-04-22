"""CPU functionality."""

import sys

read_file = sys.argv[1]

# List of instructions

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
ST = 0b10000100
AND = 0b10101000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.running = True

        # initalizing the branch table to allow O(1) runtime
        self.branchtable = {}
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[ST] = self.ST
        self.branchtable[AND] = self.AND

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
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
        pass

    def CMP(self):
        pass

    def DEC(self):
        pass

    def DIV(self):
        pass

    def HLT(self):
        # set running to False so the while loop in run() will exit
        self.running = False

    def LDI(self):
        # get the register to which the value will be saved
        reg_a = self.ram_read(self.pc + 1)
        # get the value to be saved
        reg_b = self.ram_read(self.pc + 2)
        # save the value to the register
        self.reg[reg_a] = reg_b

    def PRN(self):
        # get the register holding the value to be printed
        reg_a = self.ram_read(self.pc + 1)
        # get the value to be printed
        reg_b = self.reg[reg_a]
        # print the value in decimal
        print(int(reg_b))

    def MUL(self):
        # get the register holding first value to be multiplied
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the second value to be multiplied
        reg_b = self.ram_read(self.pc + 2)
        # preform the multiplication using ALU
        self.alu('MUL', reg_a, reg_b)

    def PUSH(self):
        # decrement SP
        self.reg[self.sp] -= 1
        # get the register holding the value to be copied
        reg_a = self.ram_read(self.pc + 1)
        # write the value in reg_a to the memory address pointed to by SP
        self.ram_write(self.reg[self.sp], self.reg[reg_a])

    def POP(self):
        # get the register that our value will be copied to
        reg_a = self.ram_read(self.pc + 1)
        # copy the value in the memory address pointed to by SP into reg_a
        self.reg[reg_a] = self.ram_read(self.reg[self.sp])
        # increment SP
        self.reg[self.sp] += 1

    def ST(self):
        # get the register holding the memory address to be written to
        reg_a = self.ram_read(self.pc + 1)
        # get the register holding the value we will be writing
        reg_b = self.ram_read(self.pc + 2)
        # write the value in reg_b to the memory address in reg_a
        self.ram_write(self.reg[reg_a], self.reg[reg_b])

    def run(self):
        """Run the CPU."""
        
        # continue to run until a HLT instruction is accessed
        while self.running:

            # get the next instruction from memory
            self.ir = self.ram_read(self.pc)
            
            # determine the amount of memory locations after that will be used
            inst_len = ((self.ir & 0b11000000) >> 6) + 1

            # preform the instruction
            self.branchtable[self.ir]()

            # increment the PC
            self.pc += inst_len
