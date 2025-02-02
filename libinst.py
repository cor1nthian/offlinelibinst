import subprocess, os, sys

# How to use:
# 1. Download required libs to a folder
#   pip download -d <lib folder path> <lib name>
#   If folder pah contains spaces, it must be quoted
# 2. Specify path to this folder either in script (targetFolder) or
#   pass this path as a second parameter
# 3. Install downloaded libs with this script

provideInstallReport = True
installSuccess = 0
installSuccessPartial = 1
installFail = 2
pipPath = '
targetFolder = ''
libExt = '.whl'
indFormat = '{:03d}'
printFmt = '%-55s%-32s'
libDict = {}
maxLibs = 256
awaitTimeout = 120000

# A python class definition for printing formatted text on terminal.
# Initialize TextFormatter object like this:
# >>> cprint = TextFormatter()
#
# Configure formatting style using .cfg method:
# >>> cprint.cfg('r', 'y', 'i')
# Argument 1: foreground(text) color
# Argument 2: background color
# Argument 3: text style
#
# Print formatted text using .out method:
# >>> cprint.out("Hello, world!")
#
# Reset to default settings using .reset method:
# >>> cprint.reset()

class TextFormatter:
    COLORCODE = {
        'k': 0,  # black
        'r': 1,  # red
        'g': 2,  # green
        'y': 3,  # yellow
        'b': 4,  # blue
        'm': 5,  # magenta
        'c': 6,  # cyan
        'w': 7   # white
    }
    FORMATCODE = {
        'b': 1,  # bold
        'f': 2,  # faint
        'i': 3,  # italic
        'u': 4,  # underline
        'x': 5,  # blinking
        'y': 6,  # fast blinking
        'r': 7,  # reverse
        'h': 8,  # hide
        's': 9,  # strikethrough
    }

    # constructor
    def __init__(self):
        self.reset()


    # function to reset properties
    def reset(self):
        # properties as dictionary
        self.prop = {'st': None, 'fg': None, 'bg': None}
        return self


    # function to configure properties
    def cfg(self, fg, bg=None, st=None):
        # reset and set all properties
        return self.reset().st(st).fg(fg).bg(bg)


    # set text style
    def st(self, st):
        if st in self.FORMATCODE.keys():
            self.prop['st'] = self.FORMATCODE[st]
        return self


    # set foreground color
    def fg(self, fg):
        if fg in self.COLORCODE.keys():
            self.prop['fg'] = 30 + self.COLORCODE[fg]
        return self


    # set background color
    def bg(self, bg):
        if bg in self.COLORCODE.keys():
            self.prop['bg'] = 40 + self.COLORCODE[bg]
        return self


    # formatting function
    def format(self, string):
        w = [self.prop['st'], self.prop['fg'], self.prop['bg']]
        w = [str(x) for x in w if x is not None]
        # return formatted string
        return '\x1b[%sm%s\x1b[0m' % (';'.join(w), string) if w else string


    # output formatted string
    def out(self, string):
        print(self.format(string))


def listFilesInFolderByExt(folderpath: str, fileext: str = libExt,
                           fullfilenames: bool = True):
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if folderpath == '':
        colorprint.out('PATH TO FOLDER IS EMPTY')
        return None
    if not os.path.exists(folderpath):
        colorprint.out('PATH TO FOLDER DOES NOT EXIST')
        return None
    filenames = []
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileext:
                if fullfilenames:
                    filenames.append(os.path.join(root, filename))
                else:
                    filenames.append(filename)
    return filenames


def installLib(libname: str):
    global pipPath, targetFolder, awaitTimeout, installSuccess, installSuccessPartial, installFail
    colorprint = TextFormatter()
    colorprint.cfg('y', 'k', 'b')
    if not os.path.exists(libname):
        colorprint.out('REQUESTED LIB DOES NOT EXIST')
        return False
    if ' ' in pipPath:
        pipPathC = '"' + pipPath + '"'
    else:
        pipPathC = pipPath
    arglist = [ pipPathC,
                'install',
                '--no-deps',
                libname ]
    arglistjoined = ' '.join(arglist)
    proc = subprocess.Popen(arglistjoined, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, universal_newlines=True)
    proc.wait(awaitTimeout)
    installRes = installFail
    out = []
    for line in proc.stdout:
        out.append(line)
    for line in out:
        lnlow = line.lower()
        if 'error' in lnlow:
            installRes = installFail
        elif 'successfully' in lnlow:
             installRes = installSuccess
    return installRes


######### SCRIPT #########
if __name__ == "__main__":
    colorprint = TextFormatter()
    colorprint.cfg('r', 'k', 'b')
    if len(pipPath) == 0 or pipPath is None:
        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                pipPath = sys.argv[1]
            else:
                colorprint.out('PATH TO PIP DOES BOT EXIST')
                systemExitCode = 1
                sys.exit(systemExitCode)
        else:
            colorprint.out('PATH TO PIP NOT SET')
            systemExitCode = 2
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(pipPath):
            colorprint.out('PATH TO PIP DOES BOT EXIST')
            systemExitCode = 1
            sys.exit(systemExitCode)
    if len(targetFolder) == 0 or targetFolder is None:
        if len(sys.argv) > 2:
            if os.path.exists(sys.argv[2]):
                targetFolder = sys.argv[2]
            else:
                colorprint.out('PATH TO TARGET FOLDER DOES BOT EXIST')
                systemExitCode = 3
                sys.exit(systemExitCode)
        else:
            colorprint.out('PATH TO TARGET FOLDER NOT SET')
            systemExitCode = 4
            sys.exit(systemExitCode)
    else:
        if not os.path.exists(targetFolder):
            colorprint.out('PATH TO TARGET FOLDER DOES BOT EXIST')
            systemExitCode = 3
            sys.exit(systemExitCode)
    if provideInstallReport is None:
        if len(sys.argv) > 3:
            provideInstallReport = bool(sys.argv[3])
        else:
            colorprint.out('INSTALL REPORT GENERATION FLAG NOT SET')
            systemExitCode = 5
            sys.exit(systemExitCode)
    if 0 >= maxLibs or maxLibs is None:
        if len(sys.argv) > 4:
            ml = int(sys.argv[4])
            if not (1024 < ml or 0 >= ml):
                maxLibs = int(sys.argv[4])
            else:
                colorprint.out('INCORRECT MAX LIB QUANTITY SET')
                systemExitCode = 6
                sys.exit(systemExitCode)
        else:
            colorprint.out('MAX LIB QUANTITY NOT SET')
            systemExitCode = 7
            sys.exit(systemExitCode)
    else:
        if 1024 < maxLibs or 0 >= maxLibs:
            colorprint.out('INCORRECT MAX LIB QUANTITY SET')
            systemExitCode = 6
            sys.exit(systemExitCode)
    libs = listFilesInFolderByExt(targetFolder)
    if libs is None or len(libs) == 0:
        colorprint.out('COULD NOT FIND ANY LIB')
        systemExitCode = 8
        sys.exit(systemExitCode)
    if len(libs) > maxLibs:
        colorprint.out('LIB QUANTITY EXCEEDED')
        systemExitCode = 9
        sys.exit(systemExitCode)
    li = 1
    installResult = installSuccess
    tlibs = len(libs)
    for lib in libs:
        indPrefix = '[' + indFormat.format(li) +' / ' +\
                       indFormat.format(tlibs) + ']'
        colorprint.out(indPrefix + ' INSTALLING ' + lib)
        installResult = installLib(lib)
        if installSuccessPartial < installResult:
            colorprint.out(indPrefix + ' FAILED INSTALLING LIB ' + lib)
        elif installSuccessPartial == installResult:
            colorprint.cfg('y', 'k', 'b')
            colorprint.out(indPrefix + ' PARTIAL SUCCESS INSTALLING LIB ' + lib)
            colorprint.cfg('r', 'k', 'b')
        elif installSuccess == installResult:
            colorprint.cfg('g', 'k', 'b')
            colorprint.out(indPrefix + ' SUCCESSFULLY INSTALLED LIB ' + lib)
            colorprint.cfg('r', 'k', 'b')
        li += 1
        if provideInstallReport:
            libDict[lib] = installResult
    if provideInstallReport:
        print(printFmt % ('Lib Name', 'Install Result'))
        for key in libDict:
            libname = key.split(os.path.sep)[-1]
            if installSuccess == libDict[key]:
                print(printFmt % (libname, 'Success'))
            elif installSuccessPartial == libDict[key]:
                print(printFmt % (libname, 'Partial success'))
            elif installFail == libDict[key]:
                print(printFmt % (libname, 'Fail'))