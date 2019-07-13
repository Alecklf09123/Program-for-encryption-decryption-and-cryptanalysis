from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import sys

#Импортируем модуль интерфейса
from last import *


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.encrypt)


    def str2bits(self,inpstr1):
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

    def spl_str(self,str,step):
        bits=[]
        str=''.join(str)
        for i in range (0,len(str),step):
            bits.append(str[i:i+step])
        return bits

    #Функция исключающего ИЛИ сообщения с ключом
    def xor_mes(self,inpstr, key ):
        bits=[]
        string=[]
        afterxor=[]
        #Добавляем нули к введенной строке
        while (len(inpstr))%(len(key))!=0:
            inpstr = '0' + inpstr
        #Ключ, равный длинне сообщения
        key=int((len(inpstr)/len(key)))*key
        afterxor=(bin(int(inpstr,2)^int(key,2)))[2:]
        while len(inpstr)!=len(afterxor):
            afterxor='0'+afterxor
        return afterxor

    #Функия s-блока
    def  s_block(self,encmes):
        lenenc=len(encmes)
        bits=[]
        finality=[]
        soobshpo8=[]
        fin=''
        #Таблица s-блока
        m={'0':{'00':'011','01':'101','10':'111','11':'100'},'1':{'00':'000','01':'010','10':'001','11':'110'}}
        #Разбиваем сообщение по 3 символа, для последующего преобразования в s-блоке
        for i in range(0, len(encmes), 3):
            bits.append(encmes[i:i+3])
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
        soobshpo8=self.spl_str(finalbits,8)
        #Преобразование двоичного кода в символ
        for i,value in enumerate(soobshpo8):
            temp=int(value,2)
            bits.append(chr(temp))
        lenencrmes=str(len(''.join(finality)))
        return finality,lenencrmes,soobshpo8,bits

    def encrypt(self):
        message=(self.ui.textBrowser.toPlainText()).split('\n')
        opT=message[0]
        encmes=self.str2bits(message[1])
        lenk=int(message[2])
        self.ui.textBrowser_2.append(f'Открытый текст : {opT}\nЗашифрованный текст : {encmes}\nДлина ключа : {lenk}\n')

        for i in range(2**lenk):
            t1=datetime.now()
            k=str(bin(i)[2:])
            while len(k)<3:
                k='0'+k
            self.ui.textBrowser_2.append(f'Ключа № {i+1} : {k}')
            bitsmes=self.str2bits(opT)
            temp=self.xor_mes(bitsmes,k)
            encryptedmes,lenencrmes,soobshpo8,bits=self.s_block("".join(temp))
            self.ui.textBrowser_2.append(f'Введённый закрытый текст :    {encmes}\nРасчитанный закрытый текст : {"".join(encryptedmes)}\n')
            encryptedmes="".join(encryptedmes)

            if encmes==encryptedmes:
                self.ui.textBrowser_2.append(f'Ключ найден : {k}')
                t2=datetime.now()
                self.ui.textBrowser_2.append(f'Ключ найден за {t2-t1}')
                break


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
