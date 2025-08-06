from abss.fs import currentProject

class Command:
    def __init__(self, args):
        self.ncomps = 2
        self.args = args[1:]
        self.manyArgs = len(self.args)
        self.rootCommand = None
        self.target = None
        self.targetType = None
        self.output = None
        self.changeField = ''
        self.datatarget = ''
        self.ref        = None
        self.options = []
        self.message = ''
        self.availableFlags = ['-o', '-r']
        self.currentFlags = {}
        if self.manyArgs > 2:
            for i in range(2, len(self.args)):
                self.options.append(args[i])

    def setReference(self, ref):
        self.ref = ref

    def setCommand(self):
        self.rootCommand = self.args[0]

    def helper(self):
        if self.rootCommand == 'apply':
            msg = """
            this command allows applying an specific data analysis method/algorithm
            dr:<algorithm>      dimension reduction ; ica, pca, tsne
            c:<algorithm>       classification
            r:<algorithm>       regression
            """
            print(msg)
        elif self.rootCommand == 'check':
            msg = """
            this command allows checking:
            -all                shows every data content
            -d -ft <filetype>   shows data of a certain type
            """
            print(msg)
        elif self.rootCommand == 'del':
            msg ="""
            this command allows deleting:
            p:<name>            projects
            d:<name>            datafile
            """
            print(msg)
        else:
            print('not available command')

    def setType(self, code):
        if code == 'p':
            self.targetType = 'project'
        elif code == 'd':
            self.targetType = 'dataproject'
        elif code == 'l':
            self.targetType = 'library'
        else:
            print('not available targetType: {}'.format(code))

    def addFlags(self):
        if '-r' in self.currentFlags:
            self.ref = self.currentFlags['-r']
        if '-o' in self.currentFlags:
            self.output = self.currentFlags['-o']

    def flagSetting(self):
        for flag in self.availableFlags:
            if(flag in self.options):
                idx = self.options.index(flag)
                if not self.args[idx+1]:
                    print('flag without arg')
                else:
                    self.currentFlags[flag] = self.options[idx + 1]
        self.addFlags()

    def setMethod(self, meth):
        if meth == 'pca':
            self.method = 'PCAnalysis'
        elif meth == 'ica':
            self.method = 'ICAnalysis'
        elif meth == 'tsne':
            self.method = 'TSNEanalysis'

    def setArgs(self):
        if self.rootCommand == 'new':
            if self.manyArgs > 1:
                cntt = self.args[1].split(':')
                self.setType(cntt[0])
                self.target = cntt[1]
                if self.manyArgs > 2:
                    self.options = self.args[1:]
            else:
                print('you need more arguments')
        elif self.rootCommand == 'current':
            if self.manyArgs == 1:
                self.options = None
            else:
                print('too much arguments')
        elif self.rootCommand == 'switch':
            if self.manyArgs > 2:
                res = self.args[1].split(':')
                self.targetType = res[0]
                self.target = res[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
            else:
                print('you need more arguments')
        elif self.rootCommand == 'check':
            if self.manyArgs > 1:
                self.options = self.args[1:]
            else:
                print('you need more arguments')
        elif self.rootCommand == 'meth':
            self.message = """

                Available Analysis
                1.PCA
                2.ICA
                3.TSNE
                4.Classification problem -> Decision Tree
                5.Classification problem -> Logistic Regression 

            """
            return self.message
        elif self.rootCommand == 'out':
            if self.manyArgs > 1:
                print('{} not allowed'.format(self.args[1:]))
                self.options = None
        elif self.rootCommand == 'change':
            if sel.manyArgs > 1:
                self.options = self.args[1:]
                idx = 0
                if 'p|name' in self.options:
                    idx = cmd.options.index('p|name')
                    self.changeField = 'datapath'
                    self.target = cmd.options(idx + 1)
                elif ('p|datapath') in self.options:
                    idx = cmd.options.index('p|datapath')
                    self.changeField = 'datapath'
                    self.target = cmd.options(idx + 1)
                else:
                    print('not changes specified')

        elif self.rootCommand == 'del':
            if self.manyArgs == 2:
                res = self.args[1].split(':')
                self.setType(res[0])
                self.target = res[1]
            elif (self.manyArgs == 1):
                self.target = currentProject()
            elif (self.manyArgs > 2):
                print('args n:',self.manyArgs)
                print('args: ', self.args)
                print('to many arguments')
            else:
                print('misterious error')

        elif self.rootCommand == 'apply':
            if self.manyArgs > 1:
                tt = self.args[1].split(':')
                if not len(tt) == 3:
                    print('command error, arguments needed')
                    sys.exit(0)
                self.targetType = tt[0]
                self.target = tt[1]
                self.setMethod(tt[2])
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
            else:
                print('you need more arguments')

    def isAvailableRootCommand(self):
        availableCommands = ['apply', 'new', 'switch', 'add', 'del', 'clean']
        if self.rootCommand in availableCommands:
            return True, 'the command is available'
        else:
            return False, 'command is not available'

