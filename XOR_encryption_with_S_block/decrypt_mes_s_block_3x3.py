from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from XOR_encryption_with_S_block import ciphers_design_decrypt
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design

class Decrypt_cipher_3x3(QtWidgets.QMainWindow,
                         ciphers_design_decrypt.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.decrypt_Button.clicked.connect(self.decrypt)

    def str2bits(self, inpstr1):
        string1 = []
        bits = []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
        for i,value in enumerate(list(inpstr1)):
            bits.append(ord(value))
            string1.append(bin(bits[i])[2:])
            while (len(string1[i]) < 8):
                string1[i] = "0" +string1[i]
        return string1

    def spl_str(self, str, step):
        bits = []
        str = ''.join(str)
        for i in range (0,len(str),step):
            bits.append(str[i:i+step])
        return bits

    #Функция исключающего ИЛИ сообщения с ключом
    def xor_mes(self, message, key):
        bits, afterxor = [], []
        #Добавляем нули к введенной строке
        while (len(message)) % (len(key)) != 0:
            message = '0' + message
        self.textBrowser_2.append(f'Введённая строка : {message}\n')
        #Ключ, равный длинне сообщения
        key = int((len(message) / len(key))) * key
        afterxor = bin(int(message, 2) ^ int(key, 2))[2:]
        while len(message) != len(afterxor):
            afterxor = '0' + afterxor
        self.textBrowser_2.append(f'Двоичная последовательность после XOR с ключом : {afterxor}\n')
        return afterxor

    def bits2str(self, finalbits):
        bits = []
        soobshpo8 = self.spl_str(finalbits, 8)
        #Преобразование двоичного кода в символ
        for i,value in enumerate(soobshpo8):
            temp = int(value,2)
            self.textBrowser_2.append(f'Код символа в ASCII-таблице: {temp}\n')
            bits.append(chr(temp))
        decrmes = ''.join(bits)
        return decrmes

    def decrypt(self):
        x = ['000','001','010','011','100','101','110','111']
        c = ['011','101','111','100','000','010','001','110']
        mes = []

        message = self.textBrowser.toPlainText().split('\n')
        opentext, key = message[0], message[1]
        mesby3bits = self.spl_str(self.str2bits(opentext), 3)

        for i in range (len(mesby3bits)):
            for j in range (len(c)):
                if mesby3bits[i] == c[j]:
                    mes.append(x[j])

        decmes = self.bits2str(self.xor_mes(''.join(mes), key))
        self.textBrowser_2.append(f'Дешифрованное сообщение: {decmes}')
        return decmes



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Decrypt_cipher_3x3()
    myapp.show()
    sys.exit(app.exec_())
