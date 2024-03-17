#!/usr/bin/env python3
# coding: utf-8

# Import libraries
from bip32utils import BIP32Key
from bitcoinlib.encoding import pubkeyhash_to_addr_bech32
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
import base58
import binascii
import ecdsa
import hashlib
import mnemonic
import pyperclip
import sys


# Class BtcWalletGen
class BtcWalletGen(QMainWindow):

    # @name: __init__()
    # @description: Class initialization
    # @return: self values
    def __init__(self):
        """ Class initialization """
        super().__init__()
        self.setWindowTitle("BtcWalletGen")
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout()

        # Title
        self.titlelayout = QHBoxLayout()
        self.titlelabel = QLabel("BTC-WalletGen")
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
            "Private WIFu",
            "Private WIFc",
            "Wallet P2PKHc",
            "Wallet P2PKH",
            "Wallet P2SHc",
            "Wallet BECH32"
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
        privkey = self.btcprivatehex(mnemon)
        pubkey = self.btcpublickey(privkey)
        wifu = self.btcprivatewifu(privkey)
        wifc = self.btcprivatewifc(privkey)
        wallet = {
            "Mnemonic": mnemon,
            "Public Key": pubkey,
            "Private Hex": privkey,
            "Private WIFu": wifu,
            "Private WIFc": wifc,
            "Wallet P2PKHc": self.walletp2pkhc(privkey),
            "Wallet P2PKH": self.walletp2pkh(privkey),
            "Wallet P2SHc": self.walletp2shc(privkey),
            "Wallet BECH32": self.walletbech32(privkey)
        }

        return wallet

    # @name: mnemonicgen()
    # @description: Generate a 12-word mnemonic
    # @return: string
    @staticmethod
    def mnemonicgen():
        """ Generate a 12-word mnemonic """
        entropy_bits = 128
        m = mnemonic.Mnemonic("english")
        words = m.generate(entropy_bits)
        return words

    # @name: btcprivatehex()
    # @description: Generate BTC private HEX key
    # @return: string
    @staticmethod
    def btcprivatehex(mnemo):
        """ Generate BTC private HEX key """
        seed = mnemonic.Mnemonic.to_seed(mnemo)
        master_key = BIP32Key.fromEntropy(seed)
        private_key = master_key.PrivateKey().hex()
        return private_key

    # @name: btcprivatewifu()
    # @description: Generate BTC private WIFu key
    # @return: string
    @staticmethod
    def btcprivatewifu(privhexkey, compressed=False):
        """ Generate BTC private WIFu key """
        if compressed:
            privhexkey += '01'
        extended_key = '80' + privhexkey
        sha256_1 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        sha256_2 = hashlib.sha256(binascii.unhexlify(sha256_1)).hexdigest()
        checksum = sha256_2[:8]
        extended_key += checksum
        wif = base58.b58encode(binascii.unhexlify(extended_key))
        wif = wif.decode("utf-8")
        return wif

    # @name: btcprivatewifc()
    # @description: Generate BTC private WIFc key
    # @return: string
    def btcprivatewifc(self, privhexkey):
        """ Generate BTC private WIFc key """
        return self.btcprivatewifu(privhexkey, compressed=True)

    # @name: btcpublickey()
    # @description: Generate BTC public key
    # @return: string
    @staticmethod
    def btcpublickey(privhexkey, compressed=True):
        """ Generate BTC public key """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        if compressed:
            cpk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
            return binascii.hexlify(cpk).decode("utf-8")
        else:
            upk = b'\x04' + vk.to_string()
            return binascii.hexlify(upk).decode("utf-8")

    # @name: walletp2pkhc()
    # @description: Generate BTC wallet address under P2PKHC format
    # @return: string
    @staticmethod
    def walletp2pkhc(privhexkey):
        """ Generate BTC wallet address under P2PKHC format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(pk).digest())
        p2pkhc = base58.b58encode_check(b'\x00' + h.digest())
        p2pkhc = p2pkhc.decode("utf-8")
        return p2pkhc

    # @name: walletp2pkh()
    # @description: Generate BTC wallet address under P2PKH format
    # @return: string
    @staticmethod
    def walletp2pkh(privhexkey):
        """ Generate BTC wallet address under P2PKH format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x04' + vk.to_string()
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(pk).digest())
        p2pkh = base58.b58encode_check(b'\x00' + h.digest())
        p2pkh = p2pkh.decode("utf-8")
        return p2pkh

    # @name: walletp2shc()
    # @description: Generate BTC wallet address under P2SHC format
    # @return: string
    @staticmethod
    def walletp2shc(privhexkey):
        """ Generate BTC wallet address under P2SHC format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
        rs = b'\x76\xa9\x14' + hashlib.new('ripemd160', hashlib.sha256(pk).digest()).digest() + b'\x88\xac'
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(rs).digest())
        p2shc = base58.b58encode_check(b'\x05' + h.digest())
        p2shc = p2shc.decode("utf-8")
        return p2shc

    # @name: walletbech32()
    # @description: Generate BTC wallet address under BECH32 format
    # @return: string
    @staticmethod
    def walletbech32(privhexkey):
        """ Generate BTC wallet address under BECH32 format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
        h = hashlib.sha256(pk).digest()
        program = binascii.unhexlify('0014') + hashlib.new('ripemd160', h).digest()
        return pubkeyhash_to_addr_bech32(program, witver=0)

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
    window = BtcWalletGen()
    window.show()
    sys.exit(app.exec())


# Callback
if __name__ == "__main__":
    main()
