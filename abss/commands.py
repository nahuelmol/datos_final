
class Command:
    def __init__(self, args):
        self.args = args
        self.manyArgs = len(args)
        self.rootCommand = None
        self.target = None
        self.targetType = None
        self.datatarget = None
        self.ref        = None
        self.options = []
        self.message = ''
        if self.manyArgs > 2:
            for i in range(2, len(self.args)):
                self.options.append(args[i])

    def setReference(self, ref):
        self.ref = ref

    def setCommand(self):
        for i in range(len(self.args)):
            if i == 1:
                self.rootCommand = self.args[i]

    def setArgs(self):
        if self.rootCommand == 'new':
            if self.manyArgs > 1:
                cntt = self.args[1].split(':')
                self.targetType = cntt[0]
                self.target = cntt[1]
                if self.manyArgs > 2:
                    self.options = self.args[2:]
            else:
                print('you need more arguments')
        elif self.rootCommand == 'switch':
            if self.manyArgs > 1:
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
                5.Ckassification problem -> Logistic Regression 

                Exit (press any) 

            """
            return self.message
        elif self.rootCommand == 'apply':
            if self.manyArgs > 1:
                tt = self.args[1].split(':')
                if not len(tt) == 3:
                    print('command error, arguments needed')
                    sys.exit()
                self.targetType = tt[0]
                self.target = tt[1]
                self.method = tt[2]
                if self.manyArgs > 2:
                    self.datatarget = self.args[2]
                    if self.manyArgs > 3:
                        self.options.append(args[3:])
                    else:
                        self.options = None
                else:
                    print('you need more arguments')
            else:
                print('you need more arguments')

            if('--t' in self.options):
                idx = self.options.index('--t')
                self.ref = self.options(idx + 1)
            else:
                print('not reference specified')
                self.ref = input('insert reference')


    def isAvailableRootCommand(self):
        availableCommands = ['new', 'switch', 'add', 'delete', 'clean']
        if self.rootCommand in availableCommands:
            print('the command is available')
        else:
            print('command is not available')

