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

def switch(cmd):
    if command.rootCommand == 'new':
        if command.targetType == 'project':
            newProject(command.target, self.options)
    elif command.rootCommand == 'del':
        if command.targetType == 'project':
            delProject(command.target, self.options)
    elif command.rootCommand == 'switch':
        if command.targetType == 'project':
            switchProject(command.target, command.options)
    elif command.rootCommand == 'check':
        checker(command)
    elif command.rootCommand == 'apply':
        if command.targetType == 'dr':
            DimReduction(command)
        elif command.targetType == 'c':
            Classification(command)
        elif command.targetType == 'r':
            Regression(command)
        else:
            print('not recognized target type')

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
    command.isAvailableRootCommand()
    command.setArgs()
    switch(command)


