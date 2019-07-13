def spl_str(str,step):
    bits=[]
    for i in range (0,len(str),step):
        bits.append(str[i:i+step])
    return bits

def str2bits(inpstr1):
    bits=[]
    string1=[]
    string2=[]
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

if __name__ == '__main__':
    lenOpT=int(input("Введите длину открытого сообщения (4-максимальная длина) : "))
    step=int((2**21)*lenOpT)
    f = open('all.txt', 'r')
    text=f.read()
    #print(len(text))

    if step<len(text):
        text=text[0:step]
        #print(len(text))
        splited=spl_str(text,lenOpT)
        #print(len(splited))
        print("MESSAGE : "+str(splited[51]))
        dvoichposl=str(str2bits(str(splited[51])))
        print("MESSAGE IN BITS : "+str(dvoichposl))

        aftx=[]
        afterxor=dvoichposl[0]
        for i in range (len(dvoichposl)):
            print(i)
            if i!=(len(dvoichposl)-1):
                print("ASD : " +str(bin(int(afterxor,2))[2:])+"  "+str(bin(int(dvoichposl[i+1],2))[2:]))
                afterxor=(bin(int(afterxor,2)^int(dvoichposl[i+1],2)))[2:]
                print("AFT X : "+str(afterxor))

            else:
                aftx.append(afterxor)
                print("Dvoichnaya posledovatelnost' : "+str(dvoichposl))
                print("Dvoichnaya posl posle xor    : "+str("".join(aftx)))
                break

    else:
        print("Введена слишком большая длина открытого текста.")
        exec
