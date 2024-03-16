#!/usr/bin/env python3
# coding: utf-8

# Import libraries
from eth_keys import keys
from eth_utils import decode_hex
from mnemonic import Mnemonic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
import hashlib
import pyperclip
import sys


# Class EthWalletGen
class EthWalletGen(QMainWindow):

    # @name: __init__()
    # @description: Class initialization
    # @return: self values
    def __init__(self):
        """ Class initialization """
        super().__init__()
        self.setWindowTitle("EthWalletGen")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Title
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel("ETH-WalletGen")
        self.title_label.setStyleSheet("font-size: 20px")
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch(1)

        # Buttons
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.walletdisplay)
        self.title_layout.addWidget(self.generate_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.title_layout.addWidget(self.close_button)
        self.layout.addLayout(self.title_layout)

        # Add separator line
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.Shape.HLine)
        separator_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addSpacing(5)
        self.layout.addWidget(separator_line)
        self.layout.addSpacing(10)

        self.outfields = {}
        self.outlabels = [
            "Mnemonic",
            "Public Key",
            "Private Hex",
            "Wallet Address"
        ]

        label_width = 100
        for fieldlabel in self.outlabels:
            label = QLabel(fieldlabel)
            label.setFixedWidth(label_width)
            self.layout.addWidget(label)
            field_layout = QHBoxLayout()
            self.outfields[fieldlabel] = QLineEdit()
            self.outfields[fieldlabel].setReadOnly(True)
            field_layout.addWidget(self.outfields[fieldlabel])
            copybtn = QPushButton("Copy")
            copytxt = self.outfields[fieldlabel].text()
            copybtn.clicked.connect(lambda _, text=copytxt, field=fieldlabel: self.copy2clipboard(text, field))
            field_layout.addWidget(copybtn)
            self.layout.addLayout(field_layout)

        # Bottom
        bottom_separator_line = QFrame()
        bottom_separator_line.setFrameShape(QFrame.Shape.HLine)
        bottom_separator_line.setFrameShadow(QFrame.Shadow.Sunken)
        bottom_separator_line.setFixedHeight(10)
        self.layout.addSpacing(5)
        self.layout.addWidget(bottom_separator_line)

        # Version
        version_layout = QHBoxLayout()
        version_label = QLabel("v1.0.2")
        version_label.setStyleSheet("font-size: 10px")
        version_label.setFixedHeight(10)
        version_layout.addStretch(1)
        version_layout.addWidget(version_label)
        self.layout.addLayout(version_layout)

        # Layout
        self.central_widget.setLayout(self.layout)

    # @name: walletdisplay()
    # @description: Return the wallet content inside the frame
    # @return: void
    def walletdisplay(self):
        """ Return the wallet content inside the frame """
        wallet_output = self.walletgen()
        for fieldlabel, value in wallet_output.items():
            self.outfields[fieldlabel].setText(value)

    # @name: walletgen()
    # @description: Generate wallet details
    # @return: array
    def walletgen(self):
        """ Generate wallet details """
        mnemon = self.mnemonicgen()
        privkey = self.ethprivatekey(mnemon)
        pubkey = self.ethpublickey(privkey)
        address = self.walleteth(pubkey)
        wallet = {
            "Mnemonic": mnemon,
            "Public Key": pubkey,
            "Private Hex": privkey,
            "Wallet Address": address
        }

        return wallet

    # @name: mnemonicgen()
    # @description: Generate a 12-word mnemonic
    # @return: string
    @staticmethod
    def mnemonicgen():
        """ Generate a 12-word mnemonic """
        mnemonic = Mnemonic("english")
        return mnemonic.generate(strength=128)

    # @name: ethprivatekey()
    # @description: Generate ETH private HEX key
    # @return: string
    @staticmethod
    def ethprivatekey(seed):
        """ Generate ETH private HEX key """
        sb = seed.encode('utf-8')
        pk = keys.PrivateKey(sb[:32])
        return pk.to_hex()

    # @name: ethpublickey()
    # @description: Generate ETH public key
    # @return: string
    @staticmethod
    def ethpublickey(privatekey):
        """ Generate ETH public key """
        pk = keys.PrivateKey(decode_hex(privatekey))
        return pk.public_key.to_hex()

    # @name: walleteth()
    # @description: Generate ETH wallet address
    # @return: string
    @staticmethod
    def walleteth(publickey):
        """ Generate ETH wallet address """
        pk = decode_hex(publickey)
        kh = hashlib.sha3_256(pk).hexdigest()
        return "0x" + kh[-40:]

    # @name: copy2clipboard()
    # @description: Copy selected text to clipboard
    # @return: void
    def copy2clipboard(self, text, label):
        """ Copy selected text to clipboard """
        pyperclip.copy(text)
        QMessageBox.information(self, "Copied", f"Content of {label} has been copied to clipboard.")


# Main function
def main():
    app = QApplication(sys.argv)
    window = EthWalletGen()
    window.show()
    sys.exit(app.exec())


# Callback
if __name__ == "__main__":
    main()
