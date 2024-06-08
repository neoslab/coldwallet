""" coding: utf-8 """

# Import libraries
from bip32utils import BIP32Key
from bitcoinlib.encoding import pubkeyhash_to_addr_bech32
from PyQt6.QtCore import QFile
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QSpacerItem
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
import base58
import binascii
import ecdsa
import hashlib
import mnemonic
import os
import platform
import sys


# Class BTCColdWallet
class BTCColdWallet(QMainWindow):

    # @name: __init__()
    # @description: Class initialization
    # @return: self values
    def __init__(self):
        """ Class initialization """
        super().__init__()

        # Define app version
        self.appversion = "1.0.3"

        # Define app compiled date
        self.appcompiled = "June 03, 2024"

        # Define app build date
        self.appbuild = "June 03, 2024"

        # Define windows value
        self.setWindowTitle("BTCColdWallet")
        self.setStyleSheet("background-color:#2a2e32;")

        # Create the menu bar
        menu_bar = self.menuBar()

        # Create "File" menu and add "Exit" action with an icon
        menu_file = menu_bar.addMenu('&File')
        action_exit = QAction(QIcon.fromTheme("system-log-out"), '&Exit', self)
        action_exit.triggered.connect(self.close)
        menu_file.addAction(action_exit)

        # Create "Help" menu and add "About" action with an icon
        menu_help = menu_bar.addMenu('&Help')
        action_about = QAction(QIcon.fromTheme("help-about"), '&About', self)
        action_about.triggered.connect(self.showabout)
        menu_help.addAction(action_about)

        # Define widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the central widget
        self.vlayout = QVBoxLayout()
        self.central_widget.setLayout(self.vlayout)

        # Create header layout
        self.header_layout = QHBoxLayout()
        self.vlayout.addSpacing(5)

        # Logo
        imgpath = None
        if platform.system() == 'Linux':
            imgpath = "resources/assets/logo/logo.png"
        elif platform.system() == 'Windows':
            imgpath = "resources\\assets\\logo\\logo.png"

        # Check if MEIPASS attribute is available in sys else return current file path
        localtmp = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        logopath = os.path.abspath(os.path.join(localtmp, imgpath))

        if QFile.exists(logopath):
            logo = QPixmap(logopath)
            if logo.isNull():
                print("Failed to load logo from", logopath)
            else:
                self.logo_label = QLabel()
                self.logo_label.setPixmap(logo.scaled(200, 28))
                self.header_layout.addWidget(self.logo_label)
        else:
            print("Logo file not found:", logopath)

        # Add a horizontal spacer
        hspacer = QSpacerItem(50, 30, QSizePolicy.Policy.Expanding)
        self.header_layout.addItem(hspacer)

        # Buttons
        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setFixedSize(100, 35)
        self.btn_generate.setStyleSheet("""
            QPushButton {
                font-size:13px;
                color:#ffffff;
                background-color:#23262a;
                border:1px solid #787878;
            }
            QPushButton:hover {
                background-color:#3a3f45;
            }
        """)
        self.btn_generate.clicked.connect(self.wallet_generator)
        self.header_layout.addWidget(self.btn_generate)

        self.btn_export = QPushButton("Export")
        self.btn_export.setFixedSize(100, 35)
        self.btn_export.setStyleSheet("""
            QPushButton {
                font-size:13px;
                color:#ffffff;
                background-color:#23262a;
                border:1px solid #787878;
            }
            QPushButton:hover {
                background-color:#3a3f45;
            }
        """)
        self.btn_export.clicked.connect(self.wallet_export)
        self.header_layout.addWidget(self.btn_export)

        # Add the "header_layout" to "vlayout"
        self.vlayout.addLayout(self.header_layout)
        self.vlayout.addSpacing(10)

        # Add a stretch to push the header to the top
        self.header_layout.addStretch(1)

        # Add the "sepline" to "vlayout"
        sepline = QFrame()
        sepline.setFrameShape(QFrame.Shape.HLine)
        sepline.setFrameShadow(QFrame.Shadow.Sunken)
        self.vlayout.addWidget(sepline)
        self.vlayout.addSpacing(5)

        # Add the "labels" and "fields"
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

        self.outfields = {}
        for fieldlabel in self.outlabels:
            label = QLabel(fieldlabel)
            label.setFixedSize(460, 30)
            label.setStyleSheet("font-size:14px;margin:0px;")
            self.vlayout.addWidget(label)
            fieldlayout = QHBoxLayout()
            self.outfields[fieldlabel] = QLineEdit()
            self.outfields[fieldlabel].setReadOnly(True)
            self.outfields[fieldlabel].setFixedSize(460, 35)
            self.outfields[fieldlabel].setStyleSheet("font-size:14px;"
                                                     "margin:0px;"
                                                     "background-color:#23262a;"
                                                     "border:1px solid #787878;")
            fieldlayout.addWidget(self.outfields[fieldlabel])
            self.vlayout.addLayout(fieldlayout)

        # Add a stretch to push the header to the top
        self.vlayout.addStretch(1)

        # Set fixed size for the main window
        self.setFixedSize(480, 830)

    # @name: wallet_generator()
    # @description: Return the wallet content inside the frame
    # @return: void
    def wallet_generator(self):
        """ Return the wallet content inside the frame """
        wallet_output = self.wallet_creator()
        for fieldlabel, value in wallet_output.items():
            self.outfields[fieldlabel].setText(value)

    # @name: wallet_creator()
    # @description: Generate wallet details
    # @return: array
    def wallet_creator(self):
        """ Generate wallet details """
        mnemonics = self.wallet_mnemonic()
        privkey = self.privatekey_hex(mnemonics)
        pubkey = self.wallet_pubkey(privkey)
        wifu = self.privatekey_wifu(privkey)
        wifc = self.privatekey_wifc(privkey)
        wallet = {
            "Mnemonic": mnemonics,
            "Public Key": pubkey,
            "Private Hex": privkey,
            "Private WIFu": wifu,
            "Private WIFc": wifc,
            "Wallet P2PKHc": self.publickey_p2pkhc(privkey),
            "Wallet P2PKH": self.publickey_p2pkh(privkey),
            "Wallet P2SHc": self.publickey_p2shc(privkey),
            "Wallet BECH32": self.publickey_bech32(privkey)
        }

        return wallet

    # @name: wallet_export()
    # @description: Export wallet data to text file
    # @return: void
    def wallet_export(self):
        """ Export BTC wallet data to text file """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            wallet_output = self.wallet_creator()
            priv_key = wallet_output["Private Hex"]
            file_name = os.path.join(folder_path, f"{priv_key}.txt")
            with open(file_name, "w") as file:
                for fieldlabel, value in wallet_output.items():
                    file.write(f"{fieldlabel}: {value}\n")
            QMessageBox.information(self, "Exported", "Wallet data exported successfully.")

    # @name: wallet_pubkey()
    # @description: Generate BTC public key
    # @return: string
    @staticmethod
    def wallet_pubkey(privhexkey, compressed=True):
        """ Generate BTC public key """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        if compressed:
            cpk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
            return binascii.hexlify(cpk).decode("utf-8")
        else:
            upk = b'\x04' + vk.to_string()
            return binascii.hexlify(upk).decode("utf-8")

    # @name: wallet_mnemonic()
    # @description: Generate a 12-word mnemonic
    # @return: string
    @staticmethod
    def wallet_mnemonic():
        """ Generate a 12-word mnemonic """
        entropy_bits = 128
        m = mnemonic.Mnemonic("english")
        words = m.generate(entropy_bits)
        return words

    # @name: privatekey_hex()
    # @description: Generate BTC private HEX key
    # @return: string
    @staticmethod
    def privatekey_hex(mnemo):
        """ Generate BTC private HEX key """
        seed = mnemonic.Mnemonic.to_seed(mnemo)
        master_key = BIP32Key.fromEntropy(seed)
        private_key = master_key.PrivateKey().hex()
        return private_key

    # @name: privatekey_wifu()
    # @description: Generate BTC private WIFu key
    # @return: string
    @staticmethod
    def privatekey_wifu(privhexkey, compressed=False):
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

    # @name: privatekey_wifc()
    # @description: Generate BTC private WIFc key
    # @return: string
    def privatekey_wifc(self, privhexkey):
        """ Generate BTC private WIFc key """
        return self.privatekey_wifu(privhexkey, compressed=True)

    # @name: publickey_p2pkhc()
    # @description: Generate BTC wallet address under P2PKHC format
    # @return: string
    @staticmethod
    def publickey_p2pkhc(privhexkey):
        """ Generate BTC wallet address under P2PKHC format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(pk).digest())
        p2pkhc = base58.b58encode_check(b'\x00' + h.digest())
        p2pkhc = p2pkhc.decode("utf-8")
        return p2pkhc

    # @name: publickey_p2pkh()
    # @description: Generate BTC wallet address under P2PKH format
    # @return: string
    @staticmethod
    def publickey_p2pkh(privhexkey):
        """ Generate BTC wallet address under P2PKH format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x04' + vk.to_string()
        h = hashlib.new('ripemd160')
        h.update(hashlib.sha256(pk).digest())
        p2pkh = base58.b58encode_check(b'\x00' + h.digest())
        p2pkh = p2pkh.decode("utf-8")
        return p2pkh

    # @name: publickey_p2shc()
    # @description: Generate BTC wallet address under P2SHC format
    # @return: string
    @staticmethod
    def publickey_p2shc(privhexkey):
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

    # @name: publickey_bech32()
    # @description: Generate BTC wallet address under BECH32 format
    # @return: string
    @staticmethod
    def publickey_bech32(privhexkey):
        """ Generate BTC wallet address under BECH32 format """
        sk = ecdsa.SigningKey.from_string(binascii.unhexlify(privhexkey), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk = b'\x02' + vk.to_string() if vk.pubkey.point.y() % 2 == 0 else b'\x03' + vk.to_string()
        h = hashlib.sha256(pk).digest()
        program = binascii.unhexlify('0014') + hashlib.new('ripemd160', h).digest()
        return pubkeyhash_to_addr_bech32(program, witver=0)

    # @name: showabout()
    # @description: Return the 'about' dialog content
    # @return: void
    def showabout(self):
        """ Return the 'about' dialog content """
        # Create a custom About dialog
        aboutdialg = QDialog(self)
        aboutdialg.setWindowTitle("About BTCColdWallet")
        aboutdialg.setWindowIcon(QIcon.fromTheme("help-about"))

        # Create layout for the dialog
        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        # Add program name label
        appname = QLabel("BTCColdWallet")
        appname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        appname.setStyleSheet("font-size:14px;font-weight:bold;padding:6px;")
        layout.addWidget(appname)

        # Add program icon (replace 'icon.png' with your actual icon file)
        imgpath = None
        if platform.system() == 'Linux':
            imgpath = "resources/assets/icon/icon.png"
        elif platform.system() == 'Windows':
            imgpath = "resources\\assets\\icon\\icon.png"

        # Check if MEIPASS attribute is available in sys else return current file path
        localtmp = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        iconpath = os.path.abspath(os.path.join(localtmp, imgpath))

        if QFile.exists(iconpath):
            icon = QPixmap(iconpath)
            if icon.isNull():
                print("Failed to load icon from", iconpath)
            else:
                applogo = QLabel()
                applogo.setPixmap(icon.scaled(128, 128))
                applogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(applogo)
        else:
            print("Icon file not found:", iconpath)

        # Add homepage information
        layout.addSpacing(10)
        homepage = QLabel("Copyright © 2002-2024")
        homepage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        homepage.setStyleSheet("font-size:14px;")
        layout.addWidget(homepage)

        # Add homepage link
        author = QLabel('<a href="https://neoslab.com">www.neoslab.com</a>')
        author.setOpenExternalLinks(True)
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setStyleSheet("font-size:14px;")
        layout.addWidget(author)
        layout.addSpacing(10)

        # Add separator line
        sepline = QFrame()
        sepline.setFrameShape(QFrame.Shape.HLine)
        sepline.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(sepline)
        layout.addSpacing(8)

        # Add build information (customize as needed)
        appsystem = None
        if platform.system() == 'Linux':
            appsystem = "Linux"
        elif platform.system() == 'Windows':
            appsystem = "Windows"

        buildinfo = QLabel("Version: {}\nCompiled for: {}\nCompiled on: {}\nBuild date: {}"
                           .format(self.appversion, appsystem, self.appcompiled, self.appbuild))
        buildinfo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        buildinfo.setStyleSheet("font-size:14px;")
        layout.addWidget(buildinfo)

        # Set the layout for the dialog
        aboutdialg.setLayout(layout)

        # Set dialog size (80% of parent window's width)
        parent_width = self.width()
        dialog_width = int(0.8 * parent_width)
        aboutdialg.setFixedSize(dialog_width, aboutdialg.height())

        # Center the dialog on the screen
        parent_pos = self.pos()
        dialog_x = parent_pos.x() + (parent_width - dialog_width) // 2
        dialog_y = parent_pos.y() + (self.height() - aboutdialg.height()) // 6
        aboutdialg.move(dialog_x, dialog_y)

        # Show the dialog
        aboutdialg.exec()


# Main function
def main():
    app = QApplication(sys.argv)
    window = BTCColdWallet()
    window.show()
    sys.exit(app.exec())


# Callback
if __name__ == "__main__":
    main()
