""" coding: utf-8 """

# Import libraries
import os
import platform
import shutil
import tempfile
from argparse import ArgumentParser


# Class Builder
class Builder(object):

    # @name: __init__()
    # @description: Class initialization
    # @param: `outputexe` the executable output name
    # @return: self values
    def __init__(self, outputexe):
        """ Class initialization """
        self.execfile = False
        self.execname = outputexe
        self.execname = os.path.basename(self.execname)
        self.worktemp = os.path.join(tempfile.gettempdir(), 'BTCColdWallet')
        self.builddir = os.path.dirname(__file__)

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
        shutil.copy('coldwallet.py', buildfile)

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
        exedata = 'bitcoinlib'
        exefile = self.execname + '.py'
        upxpath = '/usr/bin/upx'

        if platform.system() == 'Linux':
            os.system('pyinstaller '
                      '--collect-data={} '
                      '--noconsole '
                      '--onefile '
                      '--add-data resources/assets/icon/icon.png:resources/assets/icon '
                      '--add-data resources/assets/logo/logo.png:resources/assets/logo '
                      '--upx-dir={} {}'
                      .format(exedata, upxpath, exefile))
        elif platform.system() == 'Windows':
            appicon = "resources\\assets\\icon\\icon.ico"
            os.system('pyinstaller '
                      '--collect-data={} '
                      '--noconsole '
                      '--onefile '
                      '--add-data resources/assets/icon/icon.png:resources/assets/icon '
                      '--add-data resources/assets/logo/logo.png:resources/assets/logo '
                      '--upx-dir={} {}'
                      .format(exedata, appicon, upxpath, exefile))
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
        print('BTCColdWallet built successfully: %s' % self.execname)


# Main function
def main():
    parser = ArgumentParser(description='Build BTCColdWallet executable')
    parser.add_argument('-o', '--output', required=True, help='executable name')
    args = parser.parse_args()
    walletgen = Builder(outputexe=args.output)
    walletgen.buildexec()


# Callback
if __name__ == '__main__':
    main()
