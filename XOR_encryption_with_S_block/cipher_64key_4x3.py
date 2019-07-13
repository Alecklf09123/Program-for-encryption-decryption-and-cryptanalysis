from random import getrandbits
from PyQt5 import QtWidgets
import sys

#Импортируем модуль интерфейса
from XOR_encryption_with_S_block import ciphers_design
#Чтобы запустить интерфейс отсюда, использовать:
#import ciphers_design

class Cipher_4x3_s_block(QtWidgets.QMainWindow,
                         ciphers_design.Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        #Событие нажатия на кнопкуу
        self.encrypt_Button.clicked.connect(self.encrypt)


    def block64bits(self, binmes):
        while (len(binmes) % 64) != 0:
            binmes = '0' + binmes
        bits = self.spl_str(binmes, 64)
        return bits

    def bits2str(self, finalbits):
        bits=[]
        soobshpo8=self.spl_str(finalbits,8)
        #Преобразование двоичного кода в символ
        for i,value in enumerate(soobshpo8):
            temp=int(value,2)
            #print('Код символа в ASCII-таблице: '+str(temp)+'\n')
            bits.append(chr(temp))
        decrmes=''.join(bits)
        return decrmes

    def spl_str(self, str, step):
        bits = []
        str = ''.join(str)
        for i in range (0, len(str), step):
            bits.append(str[i:i+step])
        return bits

    def xor_mes(self, inpstr, key):
        bits, string, afterxor= [], [], []
        while (len(inpstr) % len(key)) != 0:
            inpstr = '0' + inpstr
        afterxor = bin(int(inpstr, 2) ^ int(key, 2))[2:]
        while len(inpstr) != len(afterxor):
            afterxor = '0' + afterxor
        return afterxor

    def round_keys(self, mainkey):
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
        mainkey = f'{bin(mainkey)[2:]:0>64}'
        temp = []
        for i in range(len(table)):
            for j in range(len(table[i])):
                temp.append(mainkey[table[i][j]])
        mainkey = ''.join(temp)

        r_keys = self.spl_str(mainkey, 4)
        #print(f'after table\n{r_keys}')
        return r_keys

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

    '''
    Сообщение разбивается на 64-битные блоки
    Каждый блок разбивается на 4-битные блоки (16 блоков)
    На основе главного ключа, равного 64 бита, формируются раундовые ключи, длиной 4 бита
    4-битный блок шифруется раундовым ключом
    Результат преобразовывается по таблице соответствующего S-блока и сдвигается влево

    Текст для шифрования и последующего криптоанализа:
    A bit harder cipher. Press button to encrypt this message!
    The second message should not be equal to the first. Enjoy
    '''
    def encrypt(self):
        message = self.textBrowser.toPlainText()
        mainkey = 8950743348026832517
        mesblocks = self.block64bits(bin(int.from_bytes(message.encode(), 'big'))[2:])
        self.textBrowser_2.append(f'Двоичный код открытого сообщения:\n{"".join(mesblocks)}')
        #self.textBrowser_2.append(f'Двоичный код сообщения, разбитого на блоки:\n{"".join(mesblocks)} \n')
        #print(f'{bin(mainkey)[2:]:0>64}')
        r_keys = self.round_keys(mainkey)

        tabl_inp, tabl_out = self.s_box()
        res = ''
        enc = []
        for i in mesblocks:
            block_4_bits = self.spl_str(i, 4)
            for j in range(len(block_4_bits)):
                aftx = self.xor_mes(block_4_bits[j], r_keys[j])
                for k in range(len(tabl_inp)):
                    #j - номер S-блока, k - индекс элемента S-блока
                    if tabl_inp[k] == aftx:
                        res = tabl_out[j][k]
                        enc.append(res)
        encryptedmes = ''.join(enc)
        #Сдвиг влево
        step = 11
        encryptedmes = encryptedmes[step:] + encryptedmes[:step]
        self.textBrowser_2.append(f'Итоговое сообщение:\n{self.bits2str(encryptedmes)}')
        self.textBrowser_2.append(f'Двоичный код зашифрованного сообщения:\n{encryptedmes}')
        encryptedmes = hex(int(encryptedmes, 2))
        self.textBrowser_2.append(f'Итоговое сообщение в hex:\n{encryptedmes}\n')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Cipher_4x3_s_block()
    myapp.show()
    sys.exit(app.exec_())
