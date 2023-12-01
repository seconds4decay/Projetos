import re
while True:
    t = input('Digite a operação: ')
    nb = re.findall('\d+', t)
    op = re.findall('[+\-*/]', t)
    a = 0
    n = len(nb)
    print(nb,op)
    opr = int(nb[0])

    for a in range(n):
        try:
            if op[a] == '+':
                opr += int(nb[a+1])
            elif op[a == '-']:
                opr -= int(nb[a+1])
            elif op[a] == '*':
                opr *= int(nb[a+1])
            elif op[a] == '/':
                opr /= int(nb[a+1])
        except IndexError:
            print(f'Resultado: {opr}')
            break
