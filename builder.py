#!/usr/bin/env python3
# coding: utf-8

# Import libraries
import os
import shutil
import tempfile
from argparse import ArgumentParser


# Class Builder
class Builder(object):

    # @name: __init__()
    # @description: Class initialization
    # @return: self values
    def __init__(self, outputexe, cryptoname):
        """ Class initialization """
        self.execfile = False
        self.execname = outputexe
        self.execname = os.path.basename(self.execname)
        self.worktemp = os.path.join(tempfile.gettempdir(), 'WalletGen')
        self.builddir = os.path.dirname(__file__)
        self.currency = cryptoname

    # @name: buildexec()
    # @description: Build the wallet generator
    # @return: boolean
    def buildexec(self):
        """ Build the wallet generator """
        # Define our template
        buildfile = 'template.py'

        # Remove previous template if exists
        if os.path.exists(buildfile):
            os.remove(buildfile)

        # Create a copy of the agent
        if self.currency == 'btc':
            shutil.copy('btcwalletgen.py', buildfile)
        elif self.currency == 'eth':
            shutil.copy('ethwalletgen.py', buildfile)
        else:
            print('This cryptocurrency is not defined')
            exit(0)

        # Check if temporary path exists
        if os.path.exists(self.worktemp):
            shutil.rmtree(self.worktemp)

        # Copy the agent directory to the temporary directory
        shutil.copytree(self.builddir, self.worktemp)

        # Get the current path
        cwd = os.getcwd()

        # Move to the temporary directory
        os.chdir(self.worktemp)

        # Move the script to the temporary directory
        shutil.move(buildfile, self.execname + '.py')

        # Create the executable using PyInstaller
        if self.currency == 'btc':
            os.system('pyinstaller --collect-data=bitcoinlib --noconsole --onefile ' + self.execname + '.py')
        elif self.currency == 'eth':
            os.system('pyinstaller --noconsole --onefile ' + self.execname + '.py')
        else:
            print('This cryptocurrency is not defined')
            exit(0)

        self.execfile = os.path.join(self.worktemp, 'dist', self.execname)

        # Return to main directory
        os.chdir(cwd)

        # Move the executable
        shutil.move(self.execfile, self.execname)

        # Delete the temporary directory
        shutil.rmtree(self.worktemp)

        # Delete the template
        os.remove(buildfile)

        # Terminate
        print('WalletGen built successfully: %s' % self.execname)


# Main function
def main():
    parser = ArgumentParser(description='Build a StopWatch executable')
    parser.add_argument('-o', '--output', required=True, help='executable name')
    parser.add_argument('-c', '--crypto', required=True, help='crypto (eth or btc)')
    args = parser.parse_args()
    walletgen = Builder(outputexe=args.output, cryptoname=args.crypto)
    walletgen.buildexec()


# Callback
if __name__ == '__main__':
    main()
