from random import getrandbits
from PyQt5 import QtWidgets
import sys
from datetime import datetime

#Импортируем модуль интерфейса
from Differential_cryptanalysis_64bit import diffdesign
#Чтобы запустить интерфейс отсюда, использовать:
#import diffdesign

class diffCryptanalysis_4x3(QtWidgets.QMainWindow,
                            diffdesign.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.pushButton.clicked.connect(self.ravensto_diff)
        self.pushButton_2.clicked.connect(self.analytics)
        self.pushButton_3.clicked.connect(self.clear_tB)

    def clear_tB(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()

    def sdvig(self, bits, step):
        length = len(bits) - step
        return bits[length:] + bits[:length]

    def spl_str(self, str, step):
        bits = []
        str = ''.join(str)
        for i in range (0, len(str), step):
            bits.append(str[i:i+step])
        return bits

    def spl_arr(self, arr, step):
         arrs = []
         while len(arr) > step:
             arrs.append(arr[:step])
             arr = arr[step:]
         arrs.append(arr)
         return arrs

    def xor_symbols(self, string1):
        #XOR посимвольно(a XOR s; a XOR d; s XOR d)
        afterxor = []
        for i in range(len(string1) - 1):
            for j in range(i + 1, len(string1)):
                afterxor.append(bin(int(string1[i], 2) ^ int(string1[j], 2))[2:])
        return afterxor

    def s_box(self):
        tabl_inp = [
        '0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111',
        '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111'
        ]
        tabl_out = [
        ['111', '010', '111', '000', '101', '110', '001', '101', '000', '100',
        '110', '011', '100', '010', '011', '001'],
        ['001', '100', '101', '101', '000', '110', '111', '010', '001', '011',
        '111', '000', '100', '011', '110', '010'],
        ['101', '001', '011', '001', '100', '111', '100', '000', '110', '101',
        '010', '010', '011', '110', '000', '111'],
        ['010', '011', '111', '110', '101', '001', '110', '000', '010', '101',
        '111', '100', '001', '000', '011', '100'],
        ['001', '000', '010', '101', '011', '111', '100', '110', '011', '111',
        '001', '110', '101', '000', '010', '100'],
        ['111', '110', '000', '011', '100', '101', '000', '111', '100', '011',
        '001', '101', '110', '010', '010', '001'],
        ['110', '100', '001', '011', '000', '010', '001', '011', '111', '101',
        '111', '010', '110', '101', '000', '100'],
        ['110', '100', '010', '101', '011', '100', '000', '110', '011', '111',
        '000', '001', '101', '001', '010', '111'],
        ['111', '000', '101', '001', '010', '110', '100', '001', '011', '000',
        '010', '110', '111', '100', '101', '011'],
        ['011', '001', '000', '101', '100', '111', '001', '000', '010', '101',
        '111', '110', '110', '011', '100', '010'],
        ['001', '001', '010', '000', '011', '101', '000', '101', '110', '010',
        '110', '111', '111', '100', '011', '100'],
        ['110', '000', '101', '111', '011', '001', '100', '111', '110', '100',
        '101', '000', '011', '010', '001', '010'],
        ['101', '011', '101', '001', '010', '100', '011', '100', '111', '000',
        '110', '001', '000', '010', '110', '111'],
        ['001', '101', '110', '100', '011', '010', '111', '110', '001', '000',
        '000', '100', '111', '010', '101', '011'],
        ['101', '100', '001', '001', '111', '000', '101', '011', '100', '010',
        '111', '011', '010', '110', '110', '000'],
        ['001', '010', '011', '001', '010', '110', '101', '101', '111', '000',
        '100', '110', '111', '100', '011', '000']
        ]
        return tabl_inp, tabl_out

    def key_analysis(self, key1, key2):
        temp = []
        for i, j in zip(key1, key2):
            if i == j:
                temp.append(i)
            if i == ' ' and j != ' ':
                temp.append(j)
            if j == ' ' and i != ' ':
                temp.append(i)
        mainkey = ''.join(temp)
        s = 0
        for i in mainkey:
            if i == '1' or i == '0':
                s += 1
        return mainkey, s

    def ravensto_diff(self):
        #textBrowser
        self.textBrowser_3.append('textBrowser: '+'\n')
        message = self.textBrowser.toPlainText().split('\n')
        opentext1, encrmes1 = message[0], message[1]
        self.textBrowser_3.append(f'Открытый текст 1: {opentext1}\nЗашифрованный текст 1: {encrmes1}\n')

        message1 = self.textBrowser_2.toPlainText().split('\n')
        opentext2, encrmes2 = message1[0], message1[1]
        self.textBrowser_3.append(f'Открытый текст 1: {opentext2}\nЗашифрованный текст 1: {encrmes2}\n')

        op_text1, enc_text1 = self.str2bits(opentext1, encrmes1)
        self.textBrowser_3.append(f'Двоичный код соответствующего символа открытого текста 1: {op_text1}\nДвоичный код соответствующего символа зашифрованного текста 1: {enc_text1}\n')

        op_bits1 = self.xor_symbols(op_text1)
        enc_bits1 = self.xor_symbols(enc_text1)

        self.textBrowser_3.append(f'Результат посимвольной операции XOR с открытым текстом: {op_bits1}\n Результат посимвольной операции XOR с текстом, после дифференцирования: {enc_bits1}\n')

        #textBrowser_2
        self.textBrowser_3.append('textBrowser2: '+'\n')
        message1 = self.textBrowser_2.toPlainText().split('\n')
        opentext2, encrmes2 = message1[0], message1[1]
        self.textBrowser_3.append(f'Открытый текст 2: {opentext2} \nЗашифрованный текст 2: {encrmes2}\n')

        op_text2, enc_text2 = self.str2bits(opentext2, encrmes2)
        self.textBrowser_3.append(f'Двоичный код соответствующего символа открытого текста 2: {op_text2}\nДвоичный код соответствующего символа зашифрованного текста 2: {enc_text2}\n')

        op_bits2 = self.xor_symbols(op_text2)
        enc_bits2 = self.xor_symbols(enc_text2)

        self.textBrowser_3.append(f'Результат посимвольной операции XOR с открытым текстом: {op_bits2}\nРезультат посимвольной операции XOR с текстом, после дифференцирования: {enc_bits2}\n')
        #Дифференциалы, без использования s-блока - равны

    def cryptanalysis(self, op_mes_blocks, enc_mes_blocks, key_lst):
        tabl_inp, tabl_out = self.s_box()
        for x, y in zip(op_mes_blocks, enc_mes_blocks):
            keyresfin = []
            for i in range(len(y)):
                keyrestemp = []
                for j in range(len(tabl_out[i])):
                    if y[i] == tabl_out[i][j]:
                        x1 = tabl_inp[j]
                        key = bin(int(x1, 2) ^ int(x[i], 2))[2:]
                        while (len(key) < 4):
                            key = '0' + key
                        keyrestemp.append(key)
                keyresfin.append(keyrestemp)
            nul, ed = '0', '1'
            keylist = []
            for j in keyresfin:
                keystr = ''
                for i in range(4):
                    snul = 0
                    sed = 0
                    for k in j:
                        if k[i] == '0':
                            snul += 1
                        else:
                            sed += 1
                    if (snul == 0) and (sed > 0):
                        keystr += '1'
                    if (sed == 0) and (snul > 0):
                        keystr += '0'
                    if (sed > 0) and (snul > 0):
                        keystr += ' '
                keylist.append(keystr)
            key = ''.join(keylist)
            key_lst.append(key)
        return key_lst

    def inputed_variables(self, opentext, encrmes):
        op_bits = opentext
        while len(op_bits) % 64 != 0:
            op_bits = '0' + op_bits
        if encrmes[:2] == '0x':
            enc_bits = bin(int(encrmes, 16))[2:]
            while len(enc_bits) % 48 != 0:
                enc_bits = '0' + enc_bits
        else:
            enc_bits = encrmes
            while len(enc_bits) % 48 != 0:
                enc_bits = '0' + enc_bits
        return op_bits, enc_bits

    def analytics(self):
        #opentext1, 2 - binary, encrmes1, 2 - binary/hex
        message = self.textBrowser.toPlainText().split('\n')
        opentext1, encrmes1 = message[0], message[1]
        op_bits1, enc_bits1 = self.inputed_variables(opentext1, encrmes1)

        message1 = self.textBrowser_2.toPlainText().split('\n')
        opentext2, encrmes2 = message1[0], message1[1]
        op_bits2, enc_bits2 = self.inputed_variables(opentext2, encrmes2)

        #Циклический сдвиг зашифрованной последовательности вправо
        enc_bits1 = self.sdvig(enc_bits1, 11)
        enc_bits2 = self.sdvig(enc_bits2, 11)

        p1 = self.spl_arr(self.spl_str(op_bits1, 4), 16)
        p2 = self.spl_arr(self.spl_str(op_bits2, 4), 16)
        self.textBrowser_3.append(f'p1 : {p1}\np2 : {p2}\n')
        c1 = self.spl_arr(self.spl_str(enc_bits1, 3), 16)
        c2 = self.spl_arr(self.spl_str(enc_bits2, 3), 16)
        self.textBrowser_3.append(f'c1 : {c1}\nc2 : {c2}\n')

        '''
        #Для построения дифференциальных таблиц распределения
        #функции в старом диф. анализе
        p1Xp2 = xor_strings(op_bits1, op_bits2)
        p1Xp2po4bits = spl_str(p1Xp2, 4)
        c1Xc2 = xor_strings(enc_bits1, enc_bits2)
        c1Xc2po3bits = spl_str(c1Xc2, 3)
        '''

        key_lst = []
        key_lst = self.cryptanalysis(p1, c1, key_lst)
        key_lst = self.cryptanalysis(p2, c2, key_lst)

        self.textBrowser_3.append(f'Таблица возможных вариантов ключа:')
        for i in key_lst:
            self.textBrowser_3.append(f'{i}')

        guessed_key = key_lst[0]
        s = 0
        for i in range(len(key_lst)):
            s += 1
            if i + 1 != len(key_lst):
                key, bits_count = self.key_analysis(guessed_key, key_lst[i + 1])
                #print(f'\ng: {guessed_key}\nt: {key_lst[i + 1]}\nk: {key}')
                self.textBrowser_3.append(f'Предполагаемый ключ: {guessed_key}\nt: {key_lst[i + 1]}\nПолучившийся ключ: {key}\n')
                guessed_key = key

        table = [
        [54, 50, 3, 1],
        [15, 63, 35, 28],
        [57, 56, 10, 17],
        [33, 7, 9, 62],
        [52, 12, 32, 20],
        [43, 14, 40, 53],
        [59, 13, 38, 39],
        [5, 36, 19, 26],
        [60, 44, 24, 58],
        [11, 41, 4, 18],
        [30, 51, 22, 16],
        [6, 23, 47, 8],
        [0, 48, 27, 34],
        [61, 37, 2, 25],
        [46, 29, 55, 49],
        [21, 42, 45, 31]
        ]

        temp = [None] * 64
        k = 0
        for i in range(len(table)):
            for j in range(len(table[i])):
                temp[table[i][j]] = key[k]
                k += 1
        key = ''.join(temp)

        #print(f'Установленно {bits_count} бита ключа')
        self.textBrowser_3.append(f'\nКлюч:\n{key}\n{"0111110000110111011011011010011011100110110101000111011010000101"}')
        self.textBrowser_3.append(f'Установленно {bits_count} бита ключа')
'''
00000000000000000000000000000000000000000000000001000001001000000110001001101001011101000010000001101000011000010111001001100100011001010111001000100000011000110110100101110000011010000110010101110010001011100010000001010000011100100110010101110011011100110010000001100010011101010111010001110100011011110110111000100000011101000110111100100000011001010110111001100011011100100111100101110000011101000010000001110100011010000110100101110011001000000110110101100101011100110111001101100001011001110110010100100001
0x527d5dc6e4c5ba3a18be5c7783823dce40df02fe78344287b30ed842e02403aa3bbe4894830a1934e4843d029bc8f181

00000000000000000000000000000000000000000000000001010100011010000110010100100000011100110110010101100011011011110110111001100100001000000110110101100101011100110111001101100001011001110110010100100000011100110110100001101111011101010110110001100100001000000110111001101111011101000010000001100010011001010010000001100101011100010111010101100001011011000010000001110100011011110010000001110100011010000110010100100000011001100110100101110010011100110111010000101110001000000100010101101110011010100110111101111001
0x527d5da05c7d3daad8425a84f306d8c042967f86fb40e4a43a3a781a407475a75f4ae025723ab93e403f026a38ca4981
'''

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = diffCryptanalysis_4x3()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
