from PyQt5 import QtWidgets
import sys
from datetime import datetime

#Импортируем модуль интерфейса
from Differential_cryptanalysis import diffdesign
#Чтобы запустить интерфейс отсюда, использовать:
#import diffdesign

class diffCryptanalysis_3x2(QtWidgets.QMainWindow,
                            diffdesign.Ui_MainWindow):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопку
        self.pushButton.clicked.connect(self.rav_diff)
        self.pushButton_2.clicked.connect(self.analytics)
        self.pushButton_3.clicked.connect(self.clear_tB)

    lst = {
    '000':{'00':0,'01':0,'10':0,'11':0},
    '001':{'00':0,'01':0,'10':0,'11':0},
    '010':{'00':0,'01':0,'10':0,'11':0},
    '011':{'00':0,'01':0,'10':0,'11':0},
    '100':{'00':0,'01':0,'10':0,'11':0},
    '101':{'00':0,'01':0,'10':0,'11':0},
    '110':{'00':0,'01':0,'10':0,'11':0},
    '111':{'00':0,'01':0,'10':0,'11':0}
    }

    #TABLICA S-Block'a
    x = ['000','001','010','011','100','101','110','111']
    c = ['11','00','10','10','01','00','11','00']

    def clear_tB(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()

    def str2bits(self, inpstr1, inpstr2):
        string1, string2, bits = [], [], []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
        for i, value in enumerate(list(inpstr1)):
            bits.append(ord(value))
            string1.append(bin(bits[i])[2:])
            while (len(string1[i]) < 8):
                string1[i] = '0' + string1[i]
        bits = []
        #Получаем ASCII-код символа, потом преобраозовываем в двоичный код, добавляя нули
        for i,value in enumerate(list(inpstr2)):
            bits.append(ord(value))
            string2.append(bin(bits[i])[2:])
            while (len(string2[i]) < 8):
                string2[i] = '0' +string2[i]
        return string1, string2

    def xor_symbols(self, string1):
        #XOR посимвольно(a XOR s; a XOR d; s XOR d)
        afterxor = []
        for i in range(len(string1) - 1):
            for j in range(i + 1, len(string1)):
                afterxor.append(bin(int(string1[i], 2) ^ int(string1[j], 2))[2:])
        return afterxor

    def xor_strings(self, string1, string2):
        afterxor = []
        for i,j in zip(string1, string2):
            temp = bin(int(i, 2) ^ int(j, 2))[2:]
            #print(f'{i} XOR {j} = {temp}')
            while (len(temp) < 8):
                temp = '0' + temp
            afterxor.append(temp)
        #print('\n')
        return afterxor

    def spl_str(self, str, step):
        bits = []
        str = ''.join(str)
        for i in range (0, len(str), step):
            bits.append(str[i : i + step])
        return bits


    #FIX THIS FUNCTION PLEASEE
    def formirovanie_tabl(self):
        finality1, finality2 = [], []
        for i in range (len(diffCryptanalysis_3x2.x)):
            for j in range (len(diffCryptanalysis_3x2.x)):
                r1 = int(diffCryptanalysis_3x2.x[i]) ^ int(diffCryptanalysis_3x2.x[j])
                r2 = int(diffCryptanalysis_3x2.c[i]) ^ int(diffCryptanalysis_3x2.c[j])
                while (len(str(r1)) < 3):
                    r1 = '0' + str(r1)
                #print(f'{diffCryptanalysis_3x2.x[i]} XOR {diffCryptanalysis_3x2.x[j]} = {r1}')
                finality1.append(str(r1))
                while (len(str(r2)) < 2):
                    r2 = '0' + str(r2)
                #print(str(c[i])+' XOR '+str(c[j])+'='+str(r2))
                finality2.append(str(r2))

        for i in range (len(finality1)):
            #print(finality1[i]+' - '+finality2[i])
            rows = finality1[i]
            cols = finality2[i]
            diffCryptanalysis_3x2.lst[rows][cols] += 1

        self.textBrowser_3.append('Дифференциальная таблица для входов и выходов:')
        cols = list(set(list([str(j) for i in diffCryptanalysis_3x2.lst.keys() for j in diffCryptanalysis_3x2.lst[i].keys()])))
        cols.sort()
        self.textBrowser_3.append('          ' + '     '.join(cols))
        for l in diffCryptanalysis_3x2.lst.keys():
            to_print = str(l) + ': '
            for k in diffCryptanalysis_3x2.lst[l].keys():
                to_print += '{:>5d}'.format(diffCryptanalysis_3x2.lst[l][k]) + '  '
            self.textBrowser_3.append(to_print)
        self.textBrowser_3.append('\n')

        self.textBrowser_3.append('Дифференциальная таблица вероятностей для входов и выходов:')
        cols = list(set(list([str(j) for i in diffCryptanalysis_3x2.lst.keys() for j in diffCryptanalysis_3x2.lst[i].keys()])))
        cols.sort()
        self.textBrowser_3.append('          ' + '     '.join(cols))
        for l in diffCryptanalysis_3x2.lst.keys():
            to_print = str(l) + ': '
            for k in diffCryptanalysis_3x2.lst[l].keys():
                diffCryptanalysis_3x2.lst[l][k] /= 8
                to_print += '{:>2.2f}'.format(diffCryptanalysis_3x2.lst[l][k]) + '  '
            self.textBrowser_3.append(to_print)
        self.textBrowser_3.append('\n')
        return diffCryptanalysis_3x2.lst

    def rav_diff(self):
        try:
            message = self.textBrowser.toPlainText().split('\n')
            op_bits1, enc_bits1 = message[0], message[1]

            message1 = self.textBrowser_2.toPlainText().split('\n')
            op_bits2, enc_bits2 = message1[0], message1[1]
        except Exception:
            op_bits1 = '001100010011010100100000011100110111100101101101011000100110111101101100011100110010000001110011011101000111001000100001'
            enc_bits1 = '111010100101100010010110101010000001010011011011101110010000001011011010101010000100110111000101101011110001111110010111'

            op_bits2 = '010101000110010101111000011101000010000001100110011011110111001000100000011000010111010001110100011000010110001101101011'
            enc_bits2 = '100011110000100011001110101011110100110111010000101101000001111110010110101110100001100111000010101110100000111011011101'
        try:
            dif_op = bin(int(op_bits1, 2) ^ int(op_bits2, 2))[2:]
            dif_enc = bin(int(enc_bits1, 2) ^ int(enc_bits2, 2))[2:]
            self.textBrowser_3.append(f'Дифференциал открытого текста:\n{dif_op}')
            self.textBrowser_3.append(f'Дифференциал зашифрованного текста:\n{dif_enc}\n')
            if dif_op == dif_enc:
                self.textBrowser_3.append(f'Дифференциалы открытых и зашифрованных текстов равны.\n')
            else:
                self.textBrowser_3.append(f'Дифференциалы открытых и зашифрованных текстов не равны.\n')
                self.textBrowser_3.append(f'Проверьте правильность введённых данных!\n')
        except Exception:
            self.textBrowser_3.append(f'Введите пары отрытых и зашифрованных сообщений в двоичном коде.\n')
        #Дифференциалы, без использования s-блока - равны
        #print(int(''.join(op_text1), 2) ^ int(''.join(op_text2), 2))
        #print(int(''.join(enc_text1), 2) ^ int(''.join(enc_text2), 2))


    def cryptanalysis(self, lst, p1, p2, c1, c2, p1Xp2po3bits, c1Xc2po3bits):
        #Из таблицы, учитывая вероятность, берем P1 Xor P2 (ключ строки) и берем C1 Xor C2 (ключ столбца)
        #Получаем варианты C1 и C2, зная результат XOR ->
        keyres1, keyres2, procentlst = [], [], []
        #TABLICA S-Block'a
        #print(f'p1 : {p1}\np2 : {p2}\nc1 : {c1}\nc2 : {c2}\n\np1Xp2po3bits : {p1Xp2po3bits}\nc1Xc2po3bits : {c1Xc2po3bits}\n')
        for i in range(len(c1Xc2po3bits)):
            procent='{:.1%}'.format(lst[str(p1Xp2po3bits[i])][str(c1Xc2po3bits[i])])
            #print (f'P1 XOR P2={p1Xp2po3bits[i]}, тогда, с вероятностью {procent} C1 XOR C2={c1Xc2po3bits[i]}')
            procentlst.append(procent)
        #print('\n')
        keyresfin = []
        #print(f'C1 : {c1}\nC2 : {c2}\nC : {diffCryptanalysis_3x2.c}\n')
        for i in range(len(c1)):
            keyrestemp = []
            for j in range(len(diffCryptanalysis_3x2.c)):
                #print('C1='+str(c1[i])+'  V TABLICE C='+str(c[j]))
                #print('C2='+str(c2[i])+'  V TABLICE C='+str(c[j]))
                if (diffCryptanalysis_3x2.c[j] == c1[i]):
                    #print(f'C1={c1[i]}  X1={diffCryptanalysis_3x2.x[j]}  P1={p1[i]}')
                    key = bin(int(diffCryptanalysis_3x2.x[j], 2) ^ int(p1[i], 2))[2:]
                    while (len(key) < 3):
                        key = '0' + key
                    keyrestemp.append(key)
                    #print(f'Key=X1 XOR P1={key}')

                if (diffCryptanalysis_3x2.c[j] == c2[i]):
                    #print(f'C2={c2[i]}  X2={diffCryptanalysis_3x2.x[j]}  P1={p2[i]}')
                    key = bin(int(diffCryptanalysis_3x2.x[j], 2) ^ int(p2[i], 2))[2:]
                    while (len(key) < 3):
                        key = '0' + key
                    keyrestemp.append(key)
                    #print(f'Key=X2 XOR P2={key}\n')
            keyresfin.append(keyrestemp)

        nul, ed = '0', '1'
        keylist = []
        for j in keyresfin:
            keystr = ''
            for i in range(3):
                snul, sed = 0, 0
                for k in j:
                    if k[i] == '0':
                        snul += 1
                    else:
                        sed += 1
                #print(f'SNUL : {snul}\nSED : {sed}')
                if (snul == 0) and (sed > 0):
                    keystr = keystr + '1'
                if (sed == 0) and (snul > 0):
                    keystr = keystr + '0'
                if (sed > 0) and (snul > 0):
                    keystr = keystr + ' '
                #print(f'KEYSTR : {keystr}\n')
            keylist.append(keystr)
        #print(f'FIN : {keyresfin}\n')
        index = 0
        for i in keylist:
            self.textBrowser_3.append(f'Предпологаемый ключ №{index+1} (с вероятностью {procentlst[index]}) :   [{i}]')
            index += 1
        self.textBrowser_3.append(f'\n')
        probablykey = ''
        for i in range(3):
            snul, sed = 0, 0
            for j in keylist:
                if j[i] == '0':
                    snul += 1
                if j[i] == '1':
                    sed += 1
            if snul == sed:
                probablykey = probablykey+' '
            if snul > sed:
                probablykey = probablykey + '0'
            if sed > snul:
                probablykey = probablykey + '1'
            self.textBrowser_3.append(f'Нулей на {i + 1}  позиции : {snul}\nЕдиниц на {i + 1}  позиции : {sed}\n')
        self.textBrowser_3.append(f'Список ключей : \n{keylist}\n')
        self.textBrowser_3.append(f'\nИтоговый ключ : {probablykey}')
        #print ('SPISOK VEROYATNOSTEY : '+str(locallist))


    def analytics(self):
        message = self.textBrowser.toPlainText().split('\n')
        opentext1, encrmes1 = message[0], message[1]
        self.textBrowser_3.append(f'Открытый текст 1: {opentext1}\nЗашифрованный текст 1: {encrmes1}\n')

        message1 = self.textBrowser_2.toPlainText().split('\n')
        opentext2, encrmes2 = message1[0], message1[1]
        self.textBrowser_3.append(f'Открытый текст 2: {opentext2}\nЗашифрованный текст 2: {encrmes2}\n')


        #XOR 2 открытых текстов
        #---------------------------------------------------------------------------

        op_bits1, enc_bits1 = self.str2bits(opentext1, encrmes1)
        op_bits2, enc_bits2 = self.str2bits(opentext2, encrmes2)

        self.textBrowser_3.append(f'{opentext1} : {op_bits1}\n{opentext2} : {op_bits2}\n')

        p1 = self.spl_str((''.join(op_bits1)), 3)
        p2 = self.spl_str((''.join(op_bits2)), 3)
        self.textBrowser_3.append(f'p1 : {p1}\np2 : {p2}\n')

        p1Xp2 = self.xor_strings(op_bits1, op_bits2)
        p1Xp2po3bits = self.spl_str(p1Xp2, 3)
        self.textBrowser_3.append(f'p1Xp2 : {p1Xp2}\np1Xp2po3bits : {p1Xp2po3bits}\n')

        self.textBrowser_3.append(f'{encrmes1} : {enc_bits1}\n{encrmes2} : {enc_bits2}\n')

        c1 = self.spl_str((''.join(enc_bits1)), 2)
        c2 = self.spl_str((''.join(enc_bits2)), 2)
        self.textBrowser_3.append(f'c1 : {c1}\nc2 : {c2}\n')

        c1Xc2 = self.xor_strings(enc_bits1, enc_bits2)
        c1Xc2po3bits = self.spl_str(c1Xc2, 2)
        self.textBrowser_3.append(f'c1Xc2 : {c1Xc2}\nc1Xc2po3bits : {c1Xc2po3bits}\n')

        lst = self.formirovanie_tabl()
        self.textBrowser_3.append(f'Таблица вероятностей S-block-a : {lst}\n')

        t1 = datetime.now()
        self.cryptanalysis(lst, p1, p2, c1, c2, p1Xp2po3bits, c1Xc2po3bits)
        t2 = datetime.now()
        self.textBrowser_3.append(f'Ключ найден за {t2-t1}\n')


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = diffCryptanalysis_3x2()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
