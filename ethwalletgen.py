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
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout()

        # Title
        self.titlelayout = QHBoxLayout()
        self.titlelabel = QLabel("ETH-WalletGen")
        self.titlelabel.setStyleSheet("font-size:18px;margin:10px 20px 10px 0px;")
        self.titlelayout.addWidget(self.titlelabel)
        self.titlelayout.addStretch(1)

        # Buttons
        self.generatebutton = QPushButton("Generate")
        self.generatebutton.clicked.connect(self.walletdisplay)
        self.titlelayout.addWidget(self.generatebutton)

        self.closebutton = QPushButton("Close")
        self.closebutton.clicked.connect(self.close)
        self.titlelayout.addWidget(self.closebutton)
        self.layout.addLayout(self.titlelayout)

        # Add separator line
        topsepline = QFrame()
        topsepline.setFrameShape(QFrame.Shape.HLine)
        topsepline.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(topsepline)
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
            fieldlayout = QHBoxLayout()
            self.outfields[fieldlabel] = QLineEdit()
            self.outfields[fieldlabel].setReadOnly(True)
            fieldlayout.addWidget(self.outfields[fieldlabel])
            copybtn = QPushButton("Copy")
            copytxt = self.outfields[fieldlabel].text()
            copybtn.clicked.connect(lambda _, text=copytxt, field=fieldlabel: self.copy2clipboard(text, field))
            fieldlayout.addWidget(copybtn)
            self.layout.addLayout(fieldlayout)

        # Bottom
        botsepline = QFrame()
        botsepline.setFrameShape(QFrame.Shape.HLine)
        botsepline.setFrameShadow(QFrame.Shadow.Sunken)
        botsepline.setFixedHeight(10)
        self.layout.addSpacing(5)
        self.layout.addWidget(botsepline)

        # Version
        verslayout = QHBoxLayout()
        verslabel = QLabel("v1.0.2")
        verslabel.setStyleSheet("font-size: 10px")
        verslabel.setFixedHeight(10)
        verslayout.addStretch(1)
        verslayout.addWidget(verslabel)
        self.layout.addLayout(verslayout)

        # Layout
        self.centralwidget.setLayout(self.layout)

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
