from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import ciphers_design_decrypt
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design_decrypt


class Decrypt_Cipher_3x3_s_block(QtWidgets.QMainWindow,
                                 ciphers_design_decrypt.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.textBrowser.append(f'Введите десятичный код зашифрованного сообщения и два ключа в двоичном коде.\n')
        #Событие нажатия на кнопкуу
        self.decrypt_Button.clicked.connect(self.decrypt)


    def str2bits(self, message):
        bits, templst = [], []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
        for i,value in enumerate(list(message)):
            bits.append(ord(value))
            message = bin(bits[i])[2:]
            templst.append(message)
            while (len(templst[i]) < 8):
                templst[i] = '0' +templst[i]
        return ''.join(templst)

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

    def spl_str(self, str, step):
        bits = []
        for i in range (0, len(''.join(str)), step):
            bits.append(str[i:i+step])
        return bits

    #Функция исключающего ИЛИ сообщения с ключом
    def xor_mes(self, message, key):
        #Добавляем нули к введенной строке
        while (len(message)) % 3 != 0:
            message = '0' + message
        lenm = len(message)
        #Ключ, равный длинне сообщения
        x = len(message) % len(key)
        if x != 0:
            key = key[-x:] + int((len(message) / len(key))) * key
        key = int((len(message) / len(key))) * key
        afterxor = bin(int(message, 2) ^ int(key, 2))[2:]
        #Добавляем нули к введенной строке
        while len(afterxor) < lenm:
            afterxor = '0' + afterxor
        return afterxor

    def S_blocks_decrypt(self, x, c, mesby3bits):
        mes = []
        for i in range (len(mesby3bits)):
            for j in range (len(c)):
                if mesby3bits[i] == c[j]:
                    mes.append(x[j])
        return ''.join(mes)

    def decrypt(self):
        x1 = ['000', '001', '010', '011', '100', '101', '110', '111']
        c1 = ['011', '101', '111', '100', '000', '010', '001', '110']
        c2 = ['010', '111', '101', '001', '000', '011', '110', '100']

        message = self.textBrowser.toPlainText().split('\n')
        opentext = bin(int(message[1]))[2:]
        key1, key2 = message[2], message[3]
        mesby3bits = self.spl_str(opentext, 3)

        mesby3bits = self.spl_str((self.xor_mes(self.S_blocks_decrypt(x1, c2, mesby3bits), key2)), 3)

        decbits = self.xor_mes(self.S_blocks_decrypt(x1, c1, mesby3bits), key1)
        self.textBrowser_2.append(f'Дешифрованное сообщение:\n\n{self.bits2str(decbits)}\n')
        self.textBrowser_2.append(f'Дешифрованное сообщение: {int(decbits, 2)}')
        return int(decbits, 2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Decrypt_Cipher_3x3_s_block()
    myapp.show()
    sys.exit(app.exec_())
