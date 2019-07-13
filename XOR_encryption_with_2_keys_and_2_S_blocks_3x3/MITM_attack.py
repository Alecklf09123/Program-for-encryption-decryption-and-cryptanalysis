from PyQt5 import QtWidgets
import sys, time

#Импортируем модуль интерфейса
from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import ciphers_design_decrypt
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design_decrypt

'''
27429947978507634
942189625772898305
6
4

30159546751659935311719658100
24391373940843913323710959874
6
4
'''

class meet_in_the_middle_attack(QtWidgets.QMainWindow,
                                ciphers_design_decrypt.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.textBrowser.append(f'Введите десятичный код открытого и '
                                f'зашифрованного сообщения и предполагаемую '
                                f'длину для 2 ключей.\n')
        #Событие нажатия на кнопкуу
        self.decrypt_Button.clicked.connect(self.workingmaking)

    def str2bits(self, message):
        bits, templst = [], []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код,
        #добавляя нули
        for i,value in enumerate(list(message)):
            bits.append(ord(value))
            message = bin(bits[i])[2:]
            templst.append(message)
            while (len(templst[i]) < 8):
                templst[i] = '0' +templst[i]
        return ''.join(templst)

    def spl_str(self, str, step):
        bits = []
        for i in range (0, len(''.join(str)), step):
            bits.append(str[i : i + step])
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

    #Функия s-блока
    def  s_block(self, encmes):
        #Таблица s-блока #1
        x = ['000', '001', '010', '011', '100', '101', '110', '111']
        c = ['011', '101', '111', '100', '000', '010', '001', '110']
        #Разбиваем сообщение по 3 символа, для последующего преобразования
        #в s-блоке
        bits = self.spl_str(encmes, 3)
        #Преобразование сообщения в s-блоке
        aft_s_box = []
        for i in bits:
            aft_s_box.append(c[x.index(i)])
        fin_bits = ''.join(aft_s_box)

        bits_for_letters = fin_bits
        #Разбивание строки по 8 бит
        while len(bits_for_letters) % 8 != 0 :
            bits_for_letters = '0' + bits_for_letters
        soobshpo8 = self.spl_str(bits_for_letters, 8)

        letters = []
        #Преобразование двоичного кода в символ
        for i, value in enumerate(soobshpo8):
            temp = int(value, 2)
            letters.append(chr(temp))
        letters = ''.join(letters)
        return letters, fin_bits

    def decrypt(self, encbits, key, x, c):
        #Разбиваем сообщение по 3 символа, для последующего преобразования
        #в s-блоке
        bits = self.spl_str(encbits, 3)
        #Преобразование сообщения в S-блоке
        aft_s_box = []
        for i in bits:
            aft_s_box.append(x[c.index(i)])
        fin_bits = ''.join(aft_s_box)
        #XOR с ключом
        mes = self.xor_mes(fin_bits, key)
        return mes

    def test(self):
        with open('results.txt', 'r') as a:
            temp = a.readlines()
        key_length, key_lst1, key_lst2  = [], [], []
        message_lst, encmes_lst = [], []
        for i in temp:
            i = i.strip().split('    ')
            key_length.append(int(i[0]))
            key_lst1.append(i[1])
            key_lst2.append(i[2])
            message_lst.append(i[3])
            encmes_lst.append(i[4])
        for opT, encmes, lenk in zip(message_lst, encmes_lst, key_length):
            bitsmes = bin(int(opT))[2:]
            encbits = bin(int(encmes))[2:]
            while (len(bitsmes)) % 3 != 0:
                bitsmes = '0' + bitsmes
            while len(encbits) != len(bitsmes):
                encbits = '0' + encbits
            keylen1, keylen2 = int(lenk), int(lenk)

            tempT2, listKeys2 = [], []

            #Таблица S-блока №2
            x2 = ['000', '001', '010', '011', '100', '101', '110', '111']
            c2 = ['010', '111', '101', '001', '000', '011', '110', '100']

            millis1 = int(round(time.time() * 1000))
            #Дешифрование итогового сообщения на всех возможных ключах
            for j in range(0, 2 ** keylen2):
                key2 = bin(j)[2:]
                while len(key2) < keylen2:
                    key2 = '0' + key2
                listKeys2.append(key2)
                tempT2.append(self.decrypt(encbits, key2, x2, c2))
            tempDict = dict(zip(tempT2, listKeys2))

            p = 0
            #Шифрование открытого сообщения и сравнивание с данными, полученными
            #в предыдущем блоке
            for i in range(0, 2 ** keylen1):
                key1 = str(bin(i)[2:])
                while len(key1) < keylen1:
                    key1 = '0' + key1
                enc = self.xor_mes(bitsmes, key1)
                encryptedmes, bits = self.s_block(enc)
                for val in tempT2:
                    if val == bits:
                        p = 1
                        millis2 = int(round(time.time() * 1000))
                        print(f'{lenk}    {key1}    {tempDict[val]}    '
                              f'{millis2 - millis1}\n')
                        break
            if p != 1:
                break

    def workingmaking(self):
        message = self.textBrowser.toPlainText().split('\n')
        #message[0] и message[1] - открытое и зашифрованное сообщение в integer
        bitsmes = bin(int(message[1]))[2:]
        encbits = bin(int(message[2]))[2:]
        while (len(bitsmes)) % 3 != 0:
            bitsmes = '0' + bitsmes
        while len(encbits) != len(bitsmes):
            encbits = '0' + encbits
        keylen1, keylen2 = int(message[3]), int(message[4])

        tempT2, listKeys2 = [], []

        #Таблица S-блока №2
        x2 = ['000', '001', '010', '011', '100', '101', '110', '111']
        c2 = ['010', '111', '101', '001', '000', '011', '110', '100']

        millis1 = int(round(time.time() * 1000))
        #Дешифрование итогового сообщения на всех возможных ключах
        for j in range(0, 2 ** keylen2):
            key2 = bin(j)[2:]
            while len(key2) < keylen2:
                key2 = '0' + key2
            listKeys2.append(key2)
            tempT2.append(self.decrypt(encbits, key2, x2, c2))
        tempDict = dict(zip(tempT2, listKeys2))

        p = 0
        #Шифрование открытого сообщения и сравнивание с данными, полученными
        #в предыдущем блоке
        for i in range(0, 2 ** keylen1):
            key1 = str(bin(i)[2:])
            while len(key1) < keylen1:
                key1 = '0' + key1
            enc = self.xor_mes(bitsmes, key1)
            encryptedmes, bits = self.s_block(enc)
            for val in tempT2:
                if val == bits:
                    p = 1
                    self.textBrowser_2.append(f'Ключ 1: {key1}\n'
                                              f'Ключ 2: {tempDict[val]}')
                    millis2 = int(round(time.time() * 1000))
                    self.textBrowser_2.append(f'Ключ найден за '
                                              f'{millis2 - millis1} '
                                              f'миллисекунд\n')
        if p != 1:
            self.textBrowser_2.append(f'Ключ не найден.\n'
                                      f'Попробуйте изменить длину ключа!')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = meet_in_the_middle_attack()
    myapp.show()
    sys.exit(app.exec_())
