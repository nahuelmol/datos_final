from abss.fs import current_project

class Command:
    def __init__(self, args):
        self.ac     = False
        self.args   = args[1:]
        self.all    = True
        self.availableCoupledFlags  = ['-o', '-r', '-n', '-me', '-mo', '-ft', 
                                       '-rs', '-ts', 'w', '-cls', 'is']
        self.availableAloneFlags    = ['-f', '-all', '-ac', '-h', '-help', 'cm']
        self.aloneFlags = {}
        self.changeField = ''
        self.class_ = 0
        self.currentFlags = {}
        self.cond = ''
        self.corr_matrix = False
        self.datatarget = ''
        self.h = False
        self.manyArgs   = len(self.args)
        self.message    = ''
        self.meth   = None
        self.mod    = None
        self.ncomps = 2
        self.number = 0
        self.random_state = 42
        self.ref        = None
        self.rootCommand = None
        self.target = None
        self.targetType = None
        self.test_size  = 0.2
        self.forced = False
        self.output = None
        self.options = []
        self.unique = False

    def setReference(self, ref):
        self.ref = ref

    def setCommand(self):
        self.rootCommand = self.args[0]

    def helper(self):
        if self.all == True:
            msg = """
            cal app
            cal ch
            cal cl
            cal del
            cal set
            """
            print(msg)
        elif self.rootCommand == 'app':
            msg = """
            cal app dr:pca -r RANK
            """
            print(msg)
        elif self.rootCommand == 'ch':
            msg = """
            cal ch meths    (all)
            cal ch meths    w pca

            cal ch mods     (all)
            cal ch mods     w log
            """
            print(msg)
        elif self.rootCommand == 'cl':
            msg = """
            cal cl meths
            cal cl meths    w pca
            cal cl meths    w pca is 1

            cal cl mods
            cal cl mods     w log
            cal cl mods     w log is 1

            cal cl exp      w cm
            cal cl exp      w cm is 1
            """
            print(msg)
        elif self.rootCommand == 'del':
            msg = """
            cal del p:heisenberg
            cal del p:all
            """
            print(msg)
        elif self.rootCommand == 'see':
            msg = """
            cal see w pca is 1
            cal see w log is 1
            """
            print(msg)
        elif self.rootCommand == 'order':
            msg = """
            cal order meths w pca
            """
            print(msg)
        else:
            True, 'not command specified'
        True, 'well provided command'

    def setType(self, code):
        if code == 'p':
            self.targetType = 'project'
        elif code == 'd':
            self.targetType = 'data'
        elif code == 'l':
            self.targetType = 'library'
        elif code == 'o':
            self.targetType = 'outputs'
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
        #here, flags activate or deactivate command variables like all, w (where), etc
        if '-r' in self.currentFlags:
            self.ref = self.currentFlags['-r']
        if '-o' in self.currentFlags:
            self.output = self.currentFlags['-o']
        if '-n' in self.currentFlags:
            self.ncomps = self.currentFlags['-n']
        if '-rs' in self.currentFlags:
            self.random_state   = float(self.currentFlags['-rs'])
        if '-ts' in self.currentFlags:
            self.test_size      = float(self.currentFlags['-ts'])
        if 'w' in self.currentFlags:
            self.all = False
            self.cond = self.currentFlags['w']
        if 'is' in self.currentFlags:
            self.all = False
            self.unique = True
            self.number = self.currentFlags['is']
        if '-cls' in self.currentFlags:
            self.class_ = int(self.currentFlags['-cls'])

        if '-ac' in self.aloneFlags:
            self.ac = True
        if '-all' in self.aloneFlags:
            self.all = True
        if '-f' in self.aloneFlags:
            self.forced = True
        if '-h' in self.aloneFlags:
            self.h = True
            self.h_cmd = self.rootCommand
        if 'cm' in self.aloneFlags:
            self.all = False
            self.corr_matrix = True

    def flagSetting(self):
        for flag in self.options:
            if flag in self.availableCoupledFlags:
                idx = self.options.index(flag)
                if not self.args[idx+1]:
                    print('{} without arg'.format(flag))
                    self.currentFlags[flag] = self.default(flag)
                else:
                    self.currentFlags[flag] = self.options[idx + 1]
            elif flag in self.availableAloneFlags:
                self.aloneFlags[flag] = True
        self.addFlags()

    def setArgs(self):
        if '-h' in self.args:
            self.h = True
            self.all = False
            return True, 'done'
        if self.rootCommand == 'app':
            if self.manyArgs > 1:
                tt = self.args[1].split(':')
                if len(tt) == 3:
                    self.targetType = tt[0]
                    self.target = tt[1]
                    self.method = tt[2]
                elif len(tt) == 2:
                    self.targetType = tt[0]
                    self.target = current_project(['datapath', 'src'])
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
        elif self.rootCommand == 'cl':
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
        elif self.rootCommand == 'xp':
            if self.manyArgs == 1:
                self.all = True
            elif self.manyArgs > 1:
                self.options = self.args[1:]
                self.flagSetting()
        elif self.rootCommand == 'see':
            if self.manyArgs > 1:
                self.options = self.args[1:]
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
        elif self.rootCommand == 'ch':
            if self.manyArgs > 1:
                self.target = self.args[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting() 
            else:
                print('you need more arguments')
        elif self.rootCommand == 'out':
            if self.manyArgs > 1:
                print('{} not allowed'.format(self.args[1:]))
                self.options = None
        elif self.rootCommand == 'change':
            if sel.manyArgs > 1:
                self.options = self.args[1:]
                idx = 0
                if 'p:name' in self.options:
                    idx = cmd.options.index('p:name')
                    self.changeField = 'datapath'
                    self.target = cmd.options(idx + 1)
                elif ('p:datapath') in self.options:
                    idx = cmd.options.index('p:datapath')
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
                self.target = current_project()
            elif (self.manyArgs > 2):
                print('args n:',self.manyArgs)
                print('args: ', self.args)
                print('to many arguments')
            else:
                print('misterious error')
        elif self.rootCommand == 'order':
            if self.manyArgs > 1:
                self.target = self.args[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
                    self.flagSetting()
        elif self.rootCommand == '-help':
            if self.manyArgs > 1:
                self.options = self.args[1:]
                self.flagSetting()
        else:
            return False, '----not recognized root'
        return True, '----args setting'

    def isAvailableRootCommand(self):
        availableCommands = ['apply', 'new', 'switch', 'add', 'del', 'cl', 'order', 'xp']
        if self.rootCommand in availableCommands:
            return True, 'the command is available'
        else:
            return False, 'command is not available'

