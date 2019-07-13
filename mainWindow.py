from PyQt5 import QtWidgets
import sys
import mainWindow_interface

from XOR_encryption_with_S_block import xor_and_s_block_3x2
from XOR_encryption_with_S_block import xor_and_s_block_3x3
from XOR_encryption_with_S_block import cipher_64key_4x3
from XOR_encryption_with_S_block import decrypt_mes_s_block_3x3

from Brute_force_search_S_block_3x3 import Brute_force_search_3x3

from Linear_cryptanalysis import linear_cipher_s_block_3x3
from Linear_cryptanalysis import linear_cipher_decrypt
from Linear_cryptanalysis import linear_cryptanalysis_S_block_3x3

from Differential_cryptanalysis import differential_cryptanalysis_S_block_3x2
from Differential_cryptanalysis import differential_cryptanalysis_S_block_3x3
from Differential_cryptanalysis_64bit import differential_cryptanalysis_S_block_4x3

from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import double_xor_cipher_3x3
from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import double_xor_decryption
from XOR_encryption_with_2_keys_and_2_S_blocks_3x3 import MITM_attack

class mainWindowApp(QtWidgets.QMainWindow,
                    mainWindow_interface.Ui_MainWindow):
    """This class implements main window of the application
    Nothing interesting happens in it's methods. Every button calls new window
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.cipher_3x2_Button.clicked.connect(
            lambda : xor_and_s_block_3x2.Cipher_3x2_s_block(self).show()
        )
        self.cipher_3x3_Button.clicked.connect(
            lambda : xor_and_s_block_3x3.Cipher_3x3_s_block(self).show()
        )
        self.hard_cipher_Button.clicked.connect(
            lambda : cipher_64key_4x3.Cipher_4x3_s_block(self).show()
        )
        self.decrypt_3x3_Button.clicked.connect(
            lambda : decrypt_mes_s_block_3x3.Decrypt_cipher_3x3(self).show()
        )


        self.brute_force_3x3_Button.clicked.connect(
            lambda : Brute_force_search_3x3.bruteForce_3x3(self).show()
        )


        self.linear_cipher_3x3_Button.clicked.connect(
            lambda : (
                linear_cipher_s_block_3x3.Linear_Cipher_3x3_s_block(self).show()
            )
        )
        self.linear_cipher_decrypt_Button.clicked.connect(
            lambda : (
                linear_cipher_decrypt.Linear_Cipher_3x3_decrypt(self).show()
            )
        )
        self.linear_crypt_3x3_Button.clicked.connect(
            lambda : (
                linear_cryptanalysis_S_block_3x3.Linear_cryptanalysis_3x3_s_block(self).show()
            )
        )


        self.differential_crypt_3x2_Button.clicked.connect(
            lambda : (
                differential_cryptanalysis_S_block_3x2.diffCryptanalysis_3x2(self).show()
            )
        )
        self.differential_crypt_3x3_Button.clicked.connect(
            lambda : (
                differential_cryptanalysis_S_block_3x3.diffCryptanalysis_3x3(self).show()
            )
        )
        self.differential_crypt_hard_cipher_Button.clicked.connect(
            lambda : (
                differential_cryptanalysis_S_block_4x3.diffCryptanalysis_4x3(self).show()
            )
        )


        self.double_cipher_3x3_Button.clicked.connect(
            lambda : (
                double_xor_cipher_3x3.Double_Cipher_3x3_s_block(self).show()
            )
        )
        self.double_cipher_decryption_Button.clicked.connect(
            lambda : (
                double_xor_decryption.Decrypt_Cipher_3x3_s_block(self).show()
                )
        )
        self.meet_in_the_middle_Button.clicked.connect(
            lambda : (
                MITM_attack.meet_in_the_middle_attack(self).show()
                )
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindowApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
