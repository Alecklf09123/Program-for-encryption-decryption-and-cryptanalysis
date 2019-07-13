from PyQt5 import QtWidgets
import sys, random, string

#Импортируем модуль интерфейса
from XOR_encryption_with_S_block import ciphers_design
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design

class Cipher_3x3_s_block(QtWidgets.QMainWindow,
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
        templst = ''.join(templst)
        return templst

    def spl_str(self, str, step):
        bits = []
        for i in range (0, len(''.join(str)), step):
            bits.append(str[i : i + step])
        return bits

    #Функция исключающего ИЛИ сообщения с ключом
    def xor_mes(self, message, key):
        bits, afterxor = [], []
        #Добавляем нули к введенной строке
        while (len(message)) % (len(key)) != 0:
            message = '0' + message
        while (len(message)) % 3 != 0:
            message = '0' + message
        self.textBrowser_2.append(f'Введённая строка : {message}\n')
        #Ключ, равный длинне сообщения
        key = int((len(message) / len(key))) * key
        afterxor = bin(int(message, 2) ^ int(key, 2))[2:]
        while len(message) != len(afterxor):
            afterxor = '0' + afterxor
        self.textBrowser_2.append(f'Двоичная последовательность после XOR '
                                  f'с ключом : {afterxor}\n')
        return afterxor

    #Функия s-блока
    def s_block(self, encmes):
        lenenc = len(encmes)
        self.textBrowser_2.append(f'Длина сообщения после операции XOR : '
                                  f'{lenenc}\n')
        #Таблица s-блока
        x = ['000', '001', '010', '011', '100', '101', '110', '111']
        c = ['011', '101', '111', '100', '000', '010', '001', '110']
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
            self.textBrowser_2.append(f'Код символа в ASCII-таблице : {temp}\n')
            letters.append(chr(temp))
        lenencrmes = str(len(fin_bits))
        return fin_bits, lenencrmes, soobshpo8, letters


    def test(self):
        with open('results.txt', 'w') as f:
            for j in range(3, 65, 1):
                key = f'{bin(random.getrandbits(j))[2:]:0>{int(j)}}'
                #print(str(key) + '     ' + str(len(key)))
                message = ''.join(random.choices(string.ascii_uppercase +
                string.ascii_lowercase + string.digits, k = 15))
                #print(message)
                bitsmes = self.str2bits(message)
                encmes = self.xor_mes(bitsmes, key)
                fin_bits, lenencrmes, soobshpo8, letters = self.s_block(
                ''.join(encmes)
                )
                letters = ''.join(letters)
                mes_in_hex = hex(int(fin_bits, 2))
                f.write(f'{len(key)}    {key}    {message}    {mes_in_hex}\n')


    def encrypt(self):
        #1948 миллисекунд
        message = self.textBrowser.toPlainText()
        key = '101001100101'
        bitsmes = self.str2bits(message)
        encmes = self.xor_mes(bitsmes, key)
        fin_bits, lenencrmes, soobshpo8, letters = self.s_block(''.join(encmes))

        self.textBrowser_2.append(f'Двоичный код зашифрованного сообщения(после'
                                  f' преобразования в s-блоке) :\n{fin_bits}\n'
                                  f'\nДлина зашифрованного сообщения :'
                                  f' {lenencrmes}\n')
        letters = ''.join(letters)
        self.textBrowser_2.append(f'Итоговое сообщение : {letters}')
        mes_in_hex = hex(int(fin_bits, 2))
        self.textBrowser_2.append(f'\nСообщение в 16-ричной сс : {mes_in_hex}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Cipher_3x3_s_block()
    myapp.show()
    sys.exit(app.exec_())
