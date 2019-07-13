from PyQt5 import QtWidgets
import sys, random, string

#Импортируем модуль интерфейса
from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import ciphers_design
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design


class Double_Cipher_3x3_s_block(QtWidgets.QMainWindow,
                                ciphers_design.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопкуу
        self.encrypt_Button.clicked.connect(self.encrypt)

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
        len_m = len(message)
        self.textBrowser_2.append(f'Введённая строка : {message}\n')
        #Ключ, равный длинне сообщения
        x = len(message) % len(key)
        if x != 0:
            key = key[-x:] + int((len(message) / len(key))) * key
        key = int((len(message) / len(key))) * key
        afterxor = bin(int(message, 2) ^ int(key, 2))[2:]
        #Добавляем нули к введенной строке
        while len(afterxor) < len_m:
            afterxor = '0' + afterxor
        self.textBrowser_2.append(f'Двоичная последовательность после XOR '
                                  f'с ключом : {afterxor}\n')
        return afterxor

    #Функия s-блока
    def  s_block(self, encmes, x, c):
        #Разбиваем сообщение по 3 символа, для последующего преобразования
        #в s-блоке
        bits = self.spl_str(encmes, 3)
        self.textBrowser_2.append(f'Список по 3 бита после операции XOR : '
                                  f'{bits}\n')
        #Преобразование сообщения в S-блоке
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

    def test(self):
        with open('results.txt', 'w') as f:
            for j in range(3, 21, 1):
                key1 = f'{bin(random.getrandbits(j))[2:]:0>{int(j)}}'
                key2 = f'{bin(random.getrandbits(j))[2:]:0>{int(j)}}'
                #print(str(key) + '     ' + str(len(key)))
                message = ''.join(random.choices(string.ascii_uppercase +
                string.ascii_lowercase + string.digits, k = 15))
                #print(message)

                #Таблицы S-блоков
                x = ['000', '001', '010', '011', '100', '101', '110', '111']
                c1 = ['011', '101', '111', '100', '000', '010', '001', '110']
                c2 = ['010', '111', '101', '001', '000', '011', '110', '100']

                tempBits1 = bin(int.from_bytes(message.encode(), 'big'))[2:]
                while (len(tempBits1)) % 3 != 0:
                    tempBits1 = '0' + tempBits1
                #Шифрование на 1 ключе, перестановка по 1 S-блоку
                tempEncmes = self.xor_mes(tempBits1, key1)
                tempEncryptedmes, tempBits2 = self.s_block(tempEncmes, x, c1)

                #Шифрование на 2 ключе, перестановка по 2 S-блоку
                encmes = self.xor_mes(tempBits2, key2)
                letters, fin_bits = self.s_block(encmes, x, c2)

                letters = ''.join(letters)
                mes_in_int = int.from_bytes(message.encode(), 'big')
                encmes_in_int = int(fin_bits, 2)
                f.write(f'{len(key1)}    {key1}    {key2}    {mes_in_int}    '
                        f'{encmes_in_int}\n')

    def encrypt(self):
        message = self.textBrowser.toPlainText()
        '''
        keylen = 16
        key1 = bin(random.getrandbits(keylen))[2:]
        key2 = bin(random.getrandbits(keylen))[2:]
        while len(key1) < keylen:
            key1 = '0' + key1
        while len(key2) < keylen:
            key2 = '0' + key2
        print(key1)
        print(key2)
        '''

        key1 = '1001'
        key2 = '0110'
        #Таблицы S-блоков
        x = ['000', '001', '010', '011', '100', '101', '110', '111']
        c1 = ['011', '101', '111', '100', '000', '010', '001', '110']
        c2 = ['010', '111', '101', '001', '000', '011', '110', '100']

        tempBits1 = bin(int.from_bytes(message.encode(), 'big'))[2:]
        while (len(tempBits1)) % 3 != 0:
            tempBits1 = '0' + tempBits1
        #Шифрование на 1 ключе, перестановка по 1 S-блоку
        tempEncmes = self.xor_mes(tempBits1, key1)
        tempEncryptedmes, tempBits2 = self.s_block(tempEncmes, x, c1)
        self.textBrowser_2.append(f'\nОткрытое сообщение : {tempBits1}\n'
                                  f'Двоичный код cообщения, после xor с первым'
                                  f' ключом : {tempBits2}')
        self.textBrowser_2.append(f'Двоичный код cообщения, после перестановок'
                                  f' в S-block 1 : {tempBits2}\n')
        self.textBrowser_2.append(f'Сообщение, после шифрования первым ключом '
                                  f': {tempEncryptedmes}\n')
        #Шифрование на 2 ключе, перестановка по 2 S-блоку
        encmes = self.xor_mes(tempBits2, key2)
        encryptedmes, bits = self.s_block(encmes, x, c2)
        self.textBrowser_2.append(f'\nДвоичный код сообщения для шифрования : '
                                  f'{tempBits2}\nДвоичный код cообщения, после'
                                  f' xor со вторым ключом : {encmes}\n'
                                  f'Двоичный код cообщения, после перестановок'
                                  f' в S-block 2 : {bits}\n'
                                  f'\nИтоговое зашифрованное сообщение : '
                                  f'{encryptedmes}\n')
        #Откытое и зашифрованное сообщение в integer, для атаки MITM
        self.textBrowser_2.append(f'{int(tempBits1, 2)}\n{int(bits, 2)}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Double_Cipher_3x3_s_block()
    myapp.show()
    sys.exit(app.exec_())
