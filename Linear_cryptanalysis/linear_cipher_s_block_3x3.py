from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from Linear_cryptanalysis import cipher_interface
#Чтобы запустить интерфейс отсюда, использовать:
#import cipher_interface

class Linear_Cipher_3x3_s_block(QtWidgets.QMainWindow,
                                cipher_interface.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.encrypt_Button.clicked.connect(self.encrypt)

    def str2bits(self, message):
        bits, templst = [], []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
        for i,value in enumerate(list(message)):
            bits.append(ord(value))
            message = bin(bits[i])[2:]
            templst.append(message)
            while (len(templst[i]) < 8):
                templst[i] = '0' +templst[i]
        templst = ''.join(templst)
        return templst

    def spl_str(self, str, step):
        bits = []
        for i in range (0, len(''.join(str)), step):
            bits.append(str[i:i+step])
        return bits

    def bits2str(self, c):
        bits = []
        #Разбивание строки по 8 бит
        soobshpo8 = self.spl_str(c, 8)
        #Преобразование двоичного кода в символ
        for i, value in enumerate(soobshpo8):
            temp = int(value, 2)
            bits.append(chr(temp))
        return ''.join(bits)

    def encrypt(self):
        message = self.textBrowser.toPlainText().split('\n')
        mes = message[0]
        key = ['1', '1', '0']
        x, c = [], []
        mesinbits = self.str2bits(mes)
        while (len(mesinbits) % 3) != 0:
            mesinbits = '0' + mesinbits
        mesby3bits = self.spl_str(mesinbits, 3)
        self.textBrowser_2.append(f'Список по 3 бита после операции XOR: {mesby3bits}\n')
        k0, k1, k2 = int(key[2]), int(key[1]), int(key[0])
        for i in mesby3bits:
            p0, p1, p2 = int(i[2]), int(i[1]), int(i[0])
            #print(f'p2 = {p2} p1 = {p1} p0 = {p0}')
            #print(f'k2 = {k2} k1 = {k1} k0 = {k0}')
            x0, x1, x2 = p0 ^ k0, p1 ^ k1, p2 ^ k2
            #print(f'x2 = {x2} x1 = {x1} x0 = {x0}\n')
            x.append(str(x2) + str(x1) + str(x0))
        for j in x:
            c0, c1, c2 = int(j[2]) ^ int(j[1]), int(j[2]) ^ int(j[1]) ^ int(j[0]), int(j[0]) ^ int(j[1])
            c.append(str(c2) + str(c1) + str(c0))
        self.textBrowser_2.append(f'x {x}\nc {c}\n')
        c = ''.join(c)
        self.textBrowser_2.append(f'Двоичный код зашифрованного сообщения (после преобразования в s-блоке): {c}\n')
        self.textBrowser_2.append(f'Итоговое сообщение: {self.bits2str(c)}\n')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Linear_Cipher_3x3_s_block()
    myapp.show()
    sys.exit(app.exec_())

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
