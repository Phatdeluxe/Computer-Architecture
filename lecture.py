import sys

# write a program in Python that runs programs

# Monday
program_filename = sys.argv[1]

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # store a value in a register (in the LS8 called LDI)
PRINT_REG = 4    # corresponds to PRN in the LS8

'''
memory = [
    PRINT_BEEJ,
    SAVE_REG,    # SAVE R0,37       store 37 in R0      the opcode
    0,   # R0       operand ("argument")
    37,  # 37       operand

    PRINT_BEEJ,

    PRINT_REG,  # PRINT_REG R0
    0,  # R0

    HALT
]
'''

memory = [0] * 256

register = [0] * 8    # like variables R0-R7

# load program into memory
address = 0
with open(program_filename) as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()

        if line == '':
            continue

        memory[address] = int(line)
        print(memory[address])
        address += 1

sys.exit()

pc = 0      # program counter, address (index) of current instruction
running = True

while running:
    inst = memory[pc]

    inst_len = ((inst & 0b11000000) >> 6) + 1

    if inst == PRINT_BEEJ:
        print('Beej!')

    elif inst == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory [pc + 2]
        register[reg_num] = value
    
    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)

    elif inst == HALT:
        running = False

    else:
        print(f'ERROR: Unknown Command {inst}')
        running = False

    pc += inst_len



# Tuesday

# Bitwise Operations

# octet == byte 
# byte == 8 bits
'''
A   B   A Bitwise-And B
-----------------------
0   0           0
0   1           0
1   0           0
1   1           1

Bitwise operators:
and: &
or:  |
not: ~
xor  ^
shift right: >>
shift left: <<


    10100100 (164)
&   10110111 (183)
------------------
    10100100 (164)


    10100100 (164)
&   11111111 (255)
------------------
    10100100 (164)


    vvvv
    10100100 (164)
&   11110000 (240)     "AND mask"
------------------
    10100000 (160)


      vv
    10100100 (164)
&   00110000 (48)     "AND mask"
------------------
    00100000 (32)


    00100000 >>
    00010000 >>     "SHIFT right"
    00001000 >>
    00000100 >>
    00000010

(10100100 & 00110000) >> 4


decimal:

      vv
    123456
    009900
    ------
    003400 >>
    000340 >>
    000034


LDI 10000010

LDI R2,37

pc += 3

       vv
ir = 0b10000010

    10000010
  & 11000000
  ----------
    10000000
    01000000
    00100000
    ...
    00000010
          ^^
    
         vvv
    00010001
  | 00000111
  ----------
    00010111
'''
