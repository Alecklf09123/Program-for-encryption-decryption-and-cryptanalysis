from PyQt5 import QtWidgets
import sys, time

#Импортируем модуль интерфейса
from Brute_force_search_S_block_3x3 import brute_force_interface
#Чтобы запустить интерфейс отсюда, использовать:
#import brute_force_interface

class bruteForce_3x3(QtWidgets.QMainWindow,
                     brute_force_interface.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.decrypt_Button.clicked.connect(self.encrypt)

        self.textBrowser_2.append(f'Введите открытый текст в символьном виде, '
                                  f'зашифрованный текст в 16-ричной сс и '
                                  f'предполанаемую длину ключа шифрования.\n')

    def str2bits(self, message):
        bits, templst = [], []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код,
        #добавляя нули
        for i, value in enumerate(list(message)):
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
    def  s_block(self, encmes):
        lenenc = len(encmes)
        #Таблица s-блока
        x = ['000', '001', '010', '011', '100', '101', '110', '111']
        c = ['011', '101', '111', '100', '000', '010', '001', '110']
        #Разбиваем сообщение по 3 символа, для последующего преобразования
        #в s-блоке
        bits = self.spl_str(encmes, 3)
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
        lenencrmes = str(len(fin_bits))
        return fin_bits, lenencrmes, soobshpo8, letters

    def test(self):
        with open('results.txt', 'r') as a:
            temp = a.readlines()
        key_length, key_lst, message_lst, encmes_lst = [], [], [], []
        for i in temp:
            i = i.strip().split('    ')
            key_length.append(int(i[0]))
            key_lst.append(i[1])
            message_lst.append(i[2])
            encmes_lst.append(i[3])
        #print(f'{key_length}\n\n{key_lst}\n\n{message_lst}\n\n{encmes_lst}')

        for opT, encmes, lenk in zip(message_lst, encmes_lst, key_length):

            encmes = bin(int(encmes, 16))[2:]
            while len(encmes) % 3 != 0:
                encmes = '0' + encmes
            bitsmes = self.str2bits(opT)

            millis1 = int(round(time.time() * 1000))
            for i in range(2 ** lenk):
                k = str(bin(i)[2:])
                while len(k) < lenk:
                    k = '0' + k

                temp = self.xor_mes(bitsmes, k)
                fin_bits, lenencrmes, soobshpo8, letters = self.s_block(
                ''.join(temp)
                )
                p = 0
                if encmes == fin_bits:
                    p = 1
                    millis2 = int(round(time.time() * 1000))
                    print(f'{lenk}    {k}    {millis2-millis1}\n')
                    break
            if p != 1:
                pass


    def encrypt(self):
        message = self.textBrowser.toPlainText().split('\n')
        opT = message[0]
        if message[1][:2] != '0x':
            self.textBrowser_2.append(f'Введите зашифрованный текст в '
                                      f'шестнадцатиричном виде!\n')
        else:
            #encmes = self.str2bits(message[1])
            encmes = bin(int(message[1], 16))[2:]
            while len(encmes) % 3 != 0:
                encmes = '0' + encmes
            bitsmes = self.str2bits(opT)
            lenk = int(message[2])
            self.textBrowser_2.append(f'Открытый текст : {opT}\n'
                                      f'Зашифрованный текст : {encmes}\n'
                                      f'Длина ключа : {lenk}\n')
            millis1 = int(round(time.time() * 1000))
            for i in range(2 ** lenk):
                k = str(bin(i)[2:])
                while len(k) < lenk:
                    k = '0' + k
                self.textBrowser_2.append(f'Ключ № {i + 1} : {k}')
                temp = self.xor_mes(bitsmes, k)
                fin_bits, lenencrmes, soobshpo8, letters = self.s_block(
                ''.join(temp)
                )
                self.textBrowser_2.append(f'Введённый закрытый текст : {encmes}'
                                          f'\nРасчитанный закрытый текст : '
                                          f'{fin_bits}\n')
                p = 0
                if encmes == fin_bits:
                    p = 1
                    self.textBrowser_2.append(f'Ключ найден : {k}')
                    millis2 = int(round(time.time() * 1000))
                    #print(f'Time spended : {millis2-millis1} milliseconds.')
                    self.textBrowser_2.append(f'Ключ найден '
                                              f'за {millis2 - millis1} '
                                              f'миллисекунд')
                    break
            if p != 1:
                self.textBrowser_2.append(f'Ключ не найден.\n'
                                          f'Попробуйте изменить длину ключа!')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = bruteForce_3x3()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
