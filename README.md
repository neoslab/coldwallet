# ColdWallet

ColdWallet is a comprehensive solution crafted in Python, comprising two powerful classes designed to empower users with the capability to generate offline Bitcoin (BTC) and Ethereum (ETH) wallets effortlessly. With ColdWallet, users can securely create wallets, obtain mnemonic phrases, private keys, public keys, and more, ensuring the utmost privacy and security for their digital assets.

* * *

#### Key Features

- Offline Generation: ColdWallet operates entirely offline, minimizing the risk of exposure to online threats such as hacking and phishing attacks. This ensures that your wallet generation process remains secure and private.
- Bitcoin (BTC) Wallet Generation: With ColdWallet, users can generate Bitcoin wallets seamlessly. Whether you're a seasoned Bitcoin enthusiast or a newcomer to the cryptocurrency space, ColdWallet simplifies the process of obtaining BTC addresses, private keys, and mnemonic phrases.
- Ethereum (ETH) Wallet Generation: Ethereum is one of the leading cryptocurrencies, and ColdWallet equips users with the tools to generate Ethereum wallets with ease. Whether you're engaging in decentralized finance (DeFi) activities or simply holding ETH, ColdWallet streamlines the process of generating ETH addresses, private keys, and mnemonic phrases. 
- Mnemonic Phrase Generation: Mnemonic phrases serve as a crucial backup mechanism for accessing your cryptocurrency funds. ColdWallet facilitates the generation of mnemonic phrases, ensuring that you have a secure and convenient way to recover your wallet in case of emergencies.
- Private Key and Public Key Extraction: ColdWallet enables users to extract both private keys and public keys from their generated wallets. This functionality is essential for performing transactions and interacting with blockchain networks securely.

#### Why Choose ColdWallet?

- Security: By operating offline, ColdWallet prioritizes the security and privacy of your digital assets, mitigating the risks associated with online vulnerabilities.
- User-Friendly Interface: ColdWallet boasts an intuitive interface, making it accessible to both novice and experienced users in the cryptocurrency space.
- Comprehensive Functionality: From wallet generation to mnemonic phrase extraction, ColdWallet offers a wide range of features to cater to your cryptocurrency needs.
- Open-Source: ColdWallet is built on open-source principles, fostering transparency and collaboration within the cryptocurrency community.

Whether you're safeguarding your Bitcoin holdings or venturing into the world of Ethereum, ColdWallet provides the tools you need to generate offline wallets securely. Experience peace of mind knowing that your digital assets are protected with ColdWallet's robust and user-friendly solution. Unlock the power of offline wallet generation with ColdWallet today!

* * *

#### Build the executable

Build the BTC ColdWallet generator on Windows

```shell
git clone https://github.com/ghostreaver/coldwallet
cd coldwallet\\BTC
python -m pip install -r requirement.txt

# To build the BTC Wallet Generator
python builder.py -o "btccoldwallet.exe"
``` 

Build the ETH ColdWallet generator on Windows

```shell
git clone https://github.com/ghostreaver/coldwallet
cd coldwallet\\ETH
python -m pip install -r requirement.txt

# To build the ETH Wallet Generator
python builder.py -o "ethcoldwallet.exe"
```

Build the BTC ColdWallet generator on Linux

```shell
git clone https://github.com/ghostreaver/coldwallet
cd coldwallet/BTC
python -m pip install -r requirement.txt

# To build the BTC Wallet Generator
python builder.py -o "btccoldwallet"
``` 

Build the ETH ColdWallet generator on Linux

```shell
git clone https://github.com/ghostreaver/coldwallet
cd coldwallet/ETH
python -m pip install -r requirement.txt

# To build the ETH Wallet Generator
python builder.py -o "ethcoldwallet"
```

* * *

#### Possible issues

```shell
Cannot find reference 'connect' in 'pyqtSignal | pyqtSignal | function'
```

To correct this bug, you will need to edit the stub file named `QtCore.pyi`, which can be found in `/site-packages/PyQt6`. After opening `QtCore.pyi`, make sure you see both of the `def connect()` lines and both of the `def emit()` lines below. If they are missing, you can add them, and the relevant warnings should disappear.

```shell
# Support for new-style signals and slots.
class pyqtSignal:

    signatures = ...    # type: typing.Tuple[str, ...]

    def __init__(self, *types: typing.Any, name: str = ...) -> None: ...

    @typing.overload
    def __get__(self, instance: None, owner: typing.Type['QObject']) -> 'pyqtSignal': ...

    @typing.overload
    def __get__(self, instance: 'QObject', owner: typing.Type['QObject']) -> 'pyqtBoundSignal': ...

    # Bug fix related to 'connect()' warning
    def connect(self, slot: 'PYQT_SLOT') -> 'QMetaObject.Connection': ...
    def emit(self, *args: typing.Any) -> None: ...
```