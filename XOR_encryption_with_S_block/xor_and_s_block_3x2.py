from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from XOR_encryption_with_S_block import ciphers_design
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design

class Cipher_3x2_s_block(QtWidgets.QMainWindow,
                         ciphers_design.Ui_MainWindow):

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

    #Функия s-блока
    def s_block(self, encmes):
        lenenc = len(encmes)
        self.textBrowser_2.append(f'Длина сообщения после операции XOR: {lenenc}\n')
        bits, finality, soobshpo8 = [], [], []
        fin = ''
        #Таблица s-блока
        m = {'0':{'00':'11','01':'00','10':'10','11':'10'},'1':{'00':'01','01':'00','10':'11','11':'00'}}
        #Разбиваем сообщение по 3 символа, для последующего преобразования в s-блоке
        for i in range(0, len(encmes), 3):
            bits.append(encmes[i:i+3])
        self.textBrowser_2.append(f'Список по 3 бита после операции XOR: {bits}\n')
        #Преобразование сообщения в s-блоке
        for i in bits:
            fin = ''
            l = i[0]
            r = i[1:]
            fin += m[l][r]
            finality.append(fin)
        finalbits = str(''.join(finality))
        bits = []
        #Разбивание строки по 8 бит
        soobshpo8 = self.spl_str(finalbits, 8)
        #Преобразование двоичного кода в символ
        for i, value in enumerate(soobshpo8):
            temp = int(value, 2)
            self.textBrowser_2.append(f'Код символа в ASCII-таблице: {temp}\n')
            bits.append(chr(temp))
        lenencrmes = str(len(''.join(finality)))
        return finality, lenencrmes, soobshpo8, bits

    def encrypt(self):
        message = self.textBrowser.toPlainText()
        key = '110'
        bitsmes = self.str2bits(message)
        encmes = self.xor_mes(bitsmes, key)
        encryptedmes, lenencrmes, soobshpo8, bits = self.s_block(''.join(encmes))

        self.textBrowser_2.append(f'Двоичный код зашифрованного сообщения(после преобразования в s-блоке): {encryptedmes} \nДлина зашифрованного сообщения: {lenencrmes}\n')
        #f = open('Cipher.txt', 'a',encoding='utf-8')
        stra = ''.join(bits)
        #f.write(stra + '\n')
        self.textBrowser_2.append(f'Итоговое сообщение: {stra}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Cipher_3x2_s_block()
    myapp.show()
    sys.exit(app.exec_())
