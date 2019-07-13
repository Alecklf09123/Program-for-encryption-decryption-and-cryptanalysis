'''
mes='011'   '110'   '111'
key='101'   '101'   '101'
xxx='110'   '011'   '010'
ccc='001'   '001'   '111'

print(list(mes))


c0=p0^k0^p1^k1
print(f'c0 {c0}')

c1=p0^k0^p1^k1^p2^k2
print(f'c1 {c1}')

c2=p1^k1^p2^k2
print(f'c2 {c2}\n')

k0=p0^(c1^c2)
k1=p1^(c0^c1^c2)
k2=p2^(c0^c1)

print(f'k0 {k0}')
print(f'k1 {k1}')
print(f'k2 {k2}')

'''

def spl_str(str, step):
    bits = []
    for i in range (0, len(str), step):
        bits.append(str[i:i+step])
    return bits

def str2bits(inpstr1):
    bits = []
    string1 = []
    lista = list(inpstr1)
    #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
    for i, value in enumerate(lista):
        bits.append(ord(value))
        inpstr1 = bin(bits[i])[2:]
        string1.append(inpstr1)
        while len(string1[i]) < 8:
            string1[i] = '0' + string1[i]
    string1 = ''.join(string1)
    return string1

def bits2str(c):
    bits=[]
    #Разбивание строки по 8 бит
    soobshpo8=spl_str(c,8)
    #Преобразование двоичного кода в символ
    for i,value in enumerate(soobshpo8):
        temp=int(value,2)
        bits.append(chr(temp))
    return ''.join(bits)

def encrypt(mes, key):

    x, c = [], []

    mesinbits = str2bits(mes)
    while (len(mesinbits) % 3) != 0:
        mesinbits = '0' + mesinbits

    mesby3bits = spl_str(mesinbits, 3)

    print(str(mesby3bits)+'\n')

    k0, k1, k2 = int(key[2]), int(key[1]), int(key[0])

    for i in mesby3bits:
        p0, p1, p2 = int(i[2]), int(i[1]), int(i[0])
        #print(f'p2 = {p2} p1 = {p1} p0 = {p0}')
        #print(f'k2 = {k2} k1 = {k1} k0 = {k0}')

        x0, x1, x2 = p0 ^ k0, p1 ^ k1, p2 ^ k2
        #print(f'x2 = {x2} x1 = {x1} x0 = {x0}\n')
        x.append(str(x2)+str(x1)+str(x0))

    for j in x:
        c0, c1, c2 = int(j[2]) ^ int(j[1]), int(j[2]) ^ int(j[1]) ^ int(j[0]), int(j[0]) ^ int(j[1])
        c.append(str(c2)+str(c1)+str(c0))
    print(f'x {x}\nc {c}')
    c=''.join(c)
    print(f'\nEncrypted message : {bits2str(c)}')

def main():
    mes = input('Type message to encrypt : ')
    key = '101'
    encrypt(mes,list(key))

if __name__ == '__main__':
    main()
