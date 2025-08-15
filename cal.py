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
from abss.fs import newProject, delProject, currentProject, outProject, switchProject
from abss.story import story_cleaner
from abss.dataSetting import setData, delData
from abss.plotViewer import seePlot
from abss.outputs import delOutputs

def switch(cmd):
    if cmd.h == True:
        cmd.helper()
        return True, 'helping'
    if cmd.rootCommand == 'apply':
        if cmd.targetType == 'dr':
            DimReduction(cmd)
        elif cmd.targetType == 'c':
            Classification(cmd)
        elif cmd.targetType == 'r':
            Regression(cmd)
        else:
            return False, 'not recognized type'
    elif cmd.rootCommand == 'change':
        res, msg = Change(cmd)
        return True, 'done'
    elif cmd.rootCommand == 'check':
        checker(cmd)
    elif cmd.rootCommand == 'current':
        currentProject()
    elif cmd.rootCommand == 'cl':
        res = story_cleaner(cmd)
        if res == False:
            return False, 'not found target to clean'
    elif cmd.rootCommand == 'del':
        if cmd.targetType == 'project':
            delProject(cmd)
        if cmd.targetType == 'data':
            delData(cmd)
        if cmd.targetType == 'outputs':
            delOutputs(cmd)
    elif cmd.rootCommand == 'new':
        if cmd.targetType == 'project':
            newProject(cmd)
    elif cmd.rootCommand == 'out':
        outProject()
    elif cmd.rootCommand == 'see':
        seePlot(cmd)
    elif cmd.rootCommand == 'sw':
        if cmd.targetType == 'project':
            switchProject(cmd)
    elif cmd.rootCommand == 'set':
        if cmd.targetType == 'data':
            setData(cmd)
    elif cmd.rootCommand == '-help':
        cmd.all == True 
        cmd.helper()
    else:
        return False, 'unrecognized command'
    return True, 'done'

if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please type a valid command'
        sys.exit(msg)
    command.setCommand()
    res, msg = command.setArgs()
    if res == True:
        print(msg)
    res, msg = switch(command)
    if res:
        print(msg)

