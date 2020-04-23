
def bin8(v):
    #             AND with 0b11111111
    #                vvv
    return f'0b{v & 0xff:08b}'
    #                    ^^^
    #     Print binary with field width 8 and pad with leading zeros

print("Signed:\n")

for i in range(8, -9, -1):
    print(f'{i:3} {bin8(i)}')

print("\nUnsigned:\n")

for i in range(8, -1, -1):
    print(f'{i:3} {bin8(i)}')
for i in range(255, 247, -1):
    print(f'{i:3} {bin8(i)}')