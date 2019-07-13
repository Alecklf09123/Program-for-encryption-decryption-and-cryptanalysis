import time

def str2bits(inpstr1):
    bits=[]
    string1=[]
    lista=list(inpstr1)
    #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
    for i,value in enumerate(lista):
        bits.append(ord(value))
        inpstr1=bin(bits[i])[2:]
        string1.append(inpstr1)
        while (len(string1[i]) < 8):
            string1[i] = '0' +string1[i]
    string1=''.join(string1)
    return string1

def spl_str(str,step):
    bits=[]
    str=''.join(str)
    for i in range (0,len(str),step):
        bits.append(str[i:i+step])
    return bits

#Функция исключающего ИЛИ сообщения с ключом
def xor_mes(inpstr, key ):
    bits=[]
    string=[]
    afterxor=[]
    #Добавляем нули к введенной строке
    while (len(inpstr))%(len(key))!=0:
        inpstr = '0' + inpstr
    #print(f'Введённая строка : {inpstr}\n')
    #Ключ, равный длинне сообщения
    key=int((len(inpstr)/len(key)))*key
    afterxor=(bin(int(inpstr,2)^int(key,2)))[2:]
    while len(inpstr)!=len(afterxor):
        afterxor='0'+afterxor
    #print(f'Двоичная последовательность после XOR с ключом : {afterxor}\n')
    return afterxor

def bits2str(finalbits):
    bits=[]
    soobshpo8=spl_str(finalbits,8)
    #Преобразование двоичного кода в символ
    for i,value in enumerate(soobshpo8):
        temp=int(value,2)
        #print('Код символа в ASCII-таблице: '+str(temp)+'\n')
        bits.append(chr(temp))
    decrmes=''.join(bits)
    return decrmes

#Функия s-блока
def  s_block(encmes):
    lenenc=len(encmes)
    #print(f'Длина сообщения после операции XOR: {lenenc}\n')
    bits=[]
    finality=[]
    soobshpo8=[]
    fin=''
    #Таблица s-блока
    m={'0':{'00':'011','01':'101','10':'111','11':'100'},'1':{'00':'000','01':'010','10':'001','11':'110'}}
    #Разбиваем сообщение по 3 символа, для последующего преобразования в s-блоке
    for i in range(0, len(encmes), 3):
        bits.append(encmes[i:i+3])
    #print(f'Список по 3 бита после операции XOR: {bits}\n')
    #Преобразование сообщения в s-блоке
    for i in bits:
        fin=''
        l=i[0]
        r=i[1:]
        fin+=m[l][r]
        finality.append(fin)
    finalbits=str(''.join(finality))
    bits=[]
    #Разбивание строки по 8 бит
    soobshpo8=spl_str(finalbits,8)
    #Преобразование двоичного кода в символ
    for i,value in enumerate(soobshpo8):
        temp=int(value,2)
        #print(f'Код символа в ASCII-таблице: {temp}\n')
        bits.append(chr(temp))
    lenencrmes=str(len(''.join(finality)))
    return finality,lenencrmes,soobshpo8,bits


def decrypt(encstring1,key):
    x=['000','001','010','011','100','101','110','111']
    c=['011','101','111','100','000','010','001','110']
    mes=[]

    encstring1inbits=str2bits(encstring1)

    encstring1po3bits=spl_str(encstring1inbits,3)
    #print("encstring1po3bits : "+str(encstring1po3bits)+'\n')

    for i in range (len(encstring1po3bits)):
        for j in range (len(c)):
            if encstring1po3bits[i]==c[j]:
                mes.append(x[j])
    mes=''.join(mes)
    mes=xor_mes(mes,key)
    decmes=bits2str(mes)
    return decmes

def workingmaking(openmes,encmes,keylen):
    tempT2=[]
    listKeys2=[]

    millis1 = int(round(time.time() * 1000))
    for j in range(0,2**keylen):

        key2=str(bin(j)[2:])
        while len(key2)<keylen:
            key2='0'+key2
        listKeys2.append(key2)
        tempT2.append(decrypt(encmes,key2))
        #print(f'Key : {key2}\nMessage : {before2key}\n')

    tempDict=dict(zip(tempT2,listKeys2))

    for i in range(0,2**keylen):

        key1=str(bin(i)[2:])
        while len(key1)<keylen:
            key1='0'+key1

        bitsmes=str2bits(openmes)
        enc=xor_mes(bitsmes,key1)
        encryptedmes,lenencrmes,soobshpo8,bits=s_block(''.join(enc))

        tempMes=''.join(bits)

        for val in tempT2:
            if val==tempMes:
                print(f'Key 1 : {key1}\nKey 2 : {tempDict[val]}')
                millis2 = int(round(time.time() * 1000))
                print(f'Time spended : {millis2-millis1} milliseconds.')

if __name__=="__main__":
    openmes=input("Open message : ")
    encmes=input("Encrypted message : ")
    lenkey=int(input("Type how much bits in key : "))
    workinmaking(openmes,encmes,lenkey)
