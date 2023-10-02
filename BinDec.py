#coversor decimal-binario e vice-versa

def dec_bin(dec: int):
    bin = []
    while dec!=0:
        bin.append(dec%2)
        dec = dec//2
    bin = bin[::-1]
    bin = "".join(map(str,bin))
    return bin

def bin_dec(bin: int):
    bin = str(bin)
    x = [int(x) for x in bin]
    x = x[::-1]
    dec = 0
    for i in range(len(bin)):
        dec += (2**i)*x[i]
    return dec

a=10
b=1010
print(dec_bin(a))
print(bin_dec(b))