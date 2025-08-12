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
        self.forced = False
        self.availableCoupledFlags  = ['-o', '-r', '-n', '-m', '-ft', '-rs', '-ts', 'w']
        self.availableAloneFlags    = ['-f', '-all', '-ac']
        self.currentFlags = {}
        self.aloneFlags = {}
        self.random_state = 42
        self.test_size = 0.2
        self.meth = None
        self.all = True
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
            self.targetType = 'data'
        elif code == 'l':
            self.targetType = 'library'
        else:
            print('not available targetType: {}'.format(code))

    def default(self, flag):
        if flag == '-n':
            return 2
        elif flag == '-r':
            return self.ref
        elif flag == 'o':
            return self.output

    def addFlags(self):
        print(self.currentFlags)
        if '-r' in self.currentFlags:
            self.ref = self.currentFlags['-r']
        if '-o' in self.currentFlags:
            self.output = self.currentFlags['-o']
        if '-n' in self.currentFlags:
            self.ncomps = self.currentFlags['-n']
        if '-m' in self.currentFlags:
            self.all    = False
            self.meth   = self.currentFlags['-m']
        if '-rs' in self.currentFlags:
            self.random_state   = float(self.currentFlags['-rs'])
        if '-ts' in self.currentFlags:
            self.test_size      = float(self.currentFlags['-ts'])
        if 'w' in self.currentFlags:
            self.all = False
            self.cond = self.currentFlags['w']

        if '-ac' in self.aloneFlags:
            self.ac = True
        if '-f' in self.aloneFlags:
            self.forced = True
        if '-all' in self.aloneFlags:
            self.all = True

    def flagSetting(self):
        for flag in self.options:
            if flag in self.availableCoupledFlags:
                idx = self.options.index(flag)
                if not self.args[idx+1]:
                    print('{} without arg'.format(flag))
                    self.currentFlags[flag] = self.default(flag)
                else:
                    self.currentFlags[flag] = self.options[idx + 1]
                    print('{}: {}'.format(flag, self.currentFlags[flag]))
            elif flag in self.availableAloneFlags:
                self.aloneFlags[flag] = True
        self.addFlags()

    def setArgs(self):
        if self.rootCommand == 'apply':
            if self.manyArgs > 1:
                tt = self.args[1].split(':')
                if len(tt) == 3:
                    self.targetType = tt[0]
                    self.target = tt[1]
                    self.method = tt[2]
                elif len(tt) == 2:
                    self.targetType = tt[0]
                    self.target = currentProject(['datapath', 'src'])
                    self.method = tt[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
            else:
                print('you need more arguments')
        elif self.rootCommand == 'new':
            if self.manyArgs > 1:
                cntt = self.args[1].split(':')
                self.setType(cntt[0])
                self.target = cntt[1]
                if self.manyArgs > 2:
                    self.options = self.args[1:]
                    self.flagSetting()
            else:
                print('you need more arguments')
        elif self.rootCommand == 'current':
            if self.manyArgs == 1:
                self.options = None
            else:
                print('too much arguments')
        elif self.rootCommand == 'clean':
            if self.manyArgs == 1:
                print('insuficient args')
            elif self.manyArgs > 1:
                self.target = self.args[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
                else:
                    self.all = True
                self.flagSetting()
        elif self.rootCommand == 'see':
            if self.manyArgs > 1:
                self.target = self.args[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
        elif self.rootCommand == 'sw':
            if self.manyArgs > 1:
                res = self.args[1].split(':')
                self.setType(res[0])
                self.target = res[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
            else:
                print('you need more arguments')
        elif self.rootCommand == 'set':
            if self.manyArgs > 1:
                res = self.args[1].split(':')
                self.setType(res[0])
                self.target = res[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
            else:
                print('you need more arguments')
        elif self.rootCommand == 'check':
            if self.manyArgs > 1:
                self.target = self.args[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting() 
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


    def isAvailableRootCommand(self):
        availableCommands = ['apply', 'new', 'switch', 'add', 'del', 'clean']
        if self.rootCommand in availableCommands:
            return True, 'the command is available'
        else:
            return False, 'command is not available'

