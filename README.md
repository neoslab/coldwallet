# CryptoSuite

CryptoSuite is a comprehensive solution crafted in Python, comprising two powerful classes designed to empower users with the capability to generate offline Bitcoin (BTC) and Ethereum (ETH) wallets effortlessly. With CryptoSuite, users can securely create wallets, obtain mnemonic phrases, private keys, public keys, and more, ensuring the utmost privacy and security for their digital assets.

* * *

#### Key Features

- Offline Generation: CryptoSuite operates entirely offline, minimizing the risk of exposure to online threats such as hacking and phishing attacks. This ensures that your wallet generation process remains secure and private.
- Bitcoin (BTC) Wallet Generation: With CryptoSuite, users can generate Bitcoin wallets seamlessly. Whether you're a seasoned Bitcoin enthusiast or a newcomer to the cryptocurrency space, CryptoSuite simplifies the process of obtaining BTC addresses, private keys, and mnemonic phrases.
- Ethereum (ETH) Wallet Generation: Ethereum is one of the leading cryptocurrencies, and CryptoSuite equips users with the tools to generate Ethereum wallets with ease. Whether you're engaging in decentralized finance (DeFi) activities or simply holding ETH, CryptoSuite streamlines the process of generating ETH addresses, private keys, and mnemonic phrases. 
- Mnemonic Phrase Generation: Mnemonic phrases serve as a crucial backup mechanism for accessing your cryptocurrency funds. CryptoSuite facilitates the generation of mnemonic phrases, ensuring that you have a secure and convenient way to recover your wallet in case of emergencies.
- Private Key and Public Key Extraction: CryptoSuite enables users to extract both private keys and public keys from their generated wallets. This functionality is essential for performing transactions and interacting with blockchain networks securely.

#### Why Choose CryptoSuite?

- Security: By operating offline, CryptoSuite prioritizes the security and privacy of your digital assets, mitigating the risks associated with online vulnerabilities.
- User-Friendly Interface: CryptoSuite boasts an intuitive interface, making it accessible to both novice and experienced users in the cryptocurrency space.
- Comprehensive Functionality: From wallet generation to mnemonic phrase extraction, CryptoSuite offers a wide range of features to cater to your cryptocurrency needs.
- Open-Source: CryptoSuite is built on open-source principles, fostering transparency and collaboration within the cryptocurrency community.

Whether you're safeguarding your Bitcoin holdings or venturing into the world of Ethereum, CryptoSuite provides the tools you need to generate offline wallets securely. Experience peace of mind knowing that your digital assets are protected with CryptoSuite's robust and user-friendly solution. Unlock the power of offline wallet generation with CryptoSuite today!

* * *

#### Build the executable

```shell
git clone https://github.com/neoslab/cryptosuite
cd cryptosuite
python3 -m pip install -r requirement.txt

# To build the BTC Wallet Generator
python3 builder.py -o "btcwalletgen" -c "btc"

# To build the ETH Wallet Generator
python3 builder.py -o "ethwalletgen" -c "eth"
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

* * * 

```shell
ValueError: unsupported hash type ripemd160
```

Hashlib uses OpenSSL for ripemd160 and apparently OpenSSL disabled some older crypto algos around version 3.0 in November 2021. All the functions are still there but require manual enabling.

```shell
# locate your SSL config file
openssl version -d
sudo nano /usr/lib/ssl/openssl.cnf
```

Ensure that the following points are configured correctly. If they are not configured as indicated below, please make the necessary modifications.

```
# List of providers to load
[provider_sect]
default = default_sect
legacy = legacy_sect

# The fips section name should match the section name inside the
# included fipsmodule.cnf.
# fips = fips_sect

# If no providers are activated explicitly, the default one is activated implicitly.
# See man 7 OSSL_PROVIDER-default for more details.
#
# If you add a section explicitly activating any other provider(s), you most
# probably need to explicitly activate the default provider, otherwise it
# becomes unavailable in openssl.  As a consequence applications depending on
# OpenSSL may not work correctly which could lead to significant system
# problems including inability to remotely access the system.
[default_sect]
activate = 1

[legacy_sect]
activate = 1
```