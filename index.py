import sys
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA

from dimreduction.kind import DimReduction
from classification.kind import Classification
from regression.kind import Regression

from data_setter import checkAvailableData, getData
from abss.commands import Command
from abss.checker import checker
from abss.change import Change
from abss.fs import newProject, delProject, currentProject, outProject

def switch(cmd):
    if cmd.rootCommand == 'apply':
        if cmd.targetType == 'dr':
            DimReduction(cmd)
        elif cmd.targetType == 'c':
            Classification(cmd)
        elif cmd.targetType == 'r':
            Regression(cmd)
        else:
            print('not recognized target type')
    elif cmd.rootCommand == 'change':
        res, msg = Change(cmd)
        print(msg)
    elif cmd.rootCommand == 'check':
        checker(cmd)
    elif cmd.rootCommand == 'current':
        currentProject()
    elif cmd.rootCommand == 'del':
        if cmd.targetType == 'project':
            delProject(cmd)
    elif cmd.rootCommand == 'new':
        if cmd.targetType == 'project':
            newProject(cmd)
    elif cmd.rootCommand == 'out':
        outProject()
    elif cmd.rootCommand == 'switch':
        if cmd.targetType == 'project':
            switchProject(cmd.target, cmd.options)
    else:
        print('unrecognized command')


if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please type a valid command'
        sys.exit(msg)
    command.setCommand()
    command.setArgs()
    switch(command)

