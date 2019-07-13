from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from Linear_cryptanalysis import cipher_interface_decrypt
#Чтобы запустить интерфейс отсюда, использовать:
#import cipher_interface_decrypt

class Linear_cryptanalysis_3x3_s_block(QtWidgets.QMainWindow,
                                       cipher_interface_decrypt.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.decrypt_Button.clicked.connect(self.analysis)

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

    def analysis(self):
        message = self.textBrowser.toPlainText().split('\n')
        mes, encmes = message[0], message[1]

        mesinbits = self.str2bits(mes)
        encmesinbits = self.str2bits(encmes)
        #encmesinbits = str2bits(encmes)
        #encmesinbits='001101010111110000011011'
        while (len(mesinbits) % 3) != 0:
            mesinbits = '0' + mesinbits
        mesby3bits = self.spl_str(mesinbits, 3)
        self.textBrowser_2.append(f'Сообщение по 3 бита: {mesby3bits}\n')
        encmesby3bits = self.spl_str(encmesinbits, 3)
        self.textBrowser_2.append(f'Список по 3 бита после операции XOR: {mesby3bits}\n')

        k = []
        #mesby3bits=['011','000','111']
        #encmesby3bits=['001','101','111']
        for i,j in zip(mesby3bits,encmesby3bits):
            p0, p1, p2 = int(i[2]), int(i[1]), int(i[0])
            c0, c1, c2 = int(j[2]), int(j[1]), int(j[0])
            k0, k1, k2 = p0 ^ (c1 ^ c2), p1 ^ (c0 ^ c1 ^ c2), p2 ^ (c0 ^ c1)

            k.append(str(k2) + str(k1) + str(k0))
        
        index = 0
        for i in k:
            self.textBrowser_2.append(f'Предпологаемый ключ №{index+1}:   [{i}]')
            index += 1
        self.textBrowser_2.append(f'\n')
        probablykey = ''
        for i in range(3):
            snul, sed = 0, 0
            for j in k:
                if j[i] == '0':
                    snul += 1
                if j[i] == '1':
                    sed += 1
            if snul == sed:
                probablykey = probablykey + ' '
            if snul > sed:
                probablykey = probablykey + '0'
            if sed > snul:
                probablykey = probablykey + '1'
            self.textBrowser_2.append(f'Нулей на {i + 1}  позиции : {snul}\nЕдиниц на {i + 1}  позиции : {sed}\n')
        self.textBrowser_2.append(f'Список ключей : \n{k}\n')
        self.textBrowser_2.append(f'\nИтоговый ключ : {probablykey}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Linear_cryptanalysis_3x3_s_block()
    myapp.show()
    sys.exit(app.exec_())
