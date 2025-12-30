import sys
import pandas as pd
import numpy as np

from dimreduction.kind import DimReduction
from classification.kind import Classification
from regression.kind import Regression
from explo.kind import ExploratoryAnalysis
from approximation.kind import Approximation

from abss.lister import list_vars, list_labs
from abss.commands import Command
from abss.change import Change
from abss.checker import checker
from abss.fs import newProject, delProject, current_project, outProject, switchProject
from abss.story import StoryCleaner, order
from abss.dataSetting import setData, delData
from abss.plotViewer import seePlot
from abss.outputs import delOutputs
from abss.glovary import setGlovar

def switch(cmd):
    if cmd.h == True:
        cmd.helper()
        return True, 'helping'
    if cmd.rootCommand == 'app':
        if cmd.targetType == 'dr':
            DimReduction(cmd)
        elif cmd.targetType == 'c':
            Classification(cmd)
        elif cmd.targetType == 'r':
            Regression(cmd)
        elif cmd.targetType == 'a':
            Approximation(cmd)
        else:
            return False, '--not recognized type'
    elif cmd.rootCommand == 'change':
        res, msg = Change(cmd)
        return True, msg
    elif cmd.rootCommand == 'ch':
        res, msg = checker(cmd)
        return True, msg
    elif cmd.rootCommand == 'current':
        msg = current_project(['project_name'])
        return True, msg
    elif cmd.rootCommand == 'cl':
        SC = StoryCleaner(cmd)
        SC.run()
        return True, SC.message
    elif cmd.rootCommand == 'del':
        if cmd.targetType == 'project':
            delProject(cmd)
        elif cmd.targetType == 'data':
            delData(cmd)
        elif cmd.targetType == 'outputs':
            delOutputs(cmd)
        else:
            return False, '----del:unknown target type'
        msg = '----del:{}:done'.format(cmd.targetType)
        return True, msg

    elif cmd.rootCommand == 'list':
        if cmd.target == 'vars':
            list_vars(cmd)
        elif cmd.target == 'labs':
            list_cols(cmd)
        else:
            return False, '----list:unknown target'
        msg = '----list:{}:done'.format(cmd.target)
        return True, msg
    elif cmd.rootCommand == 'xp':
        res, msg = ExploratoryAnalysis(cmd)
        return True, msg
    elif cmd.rootCommand == 'new':
        if cmd.targetType == 'project':
            newProject(cmd)
            return True, '----new:project:done'
    elif cmd.rootCommand == 'out':
        outProject()
        return True, '----out:project:done'
    elif cmd.rootCommand == 'see':
        seePlot(cmd)
        return True, '----see:project:done'
    elif cmd.rootCommand == 'sw':
        if cmd.targetType == 'project':
            switchProject(cmd)
        else:
            return False, '----switch:unknown'
        msg = '----switch:{}:done'.format(cmd.targetType)
        return True, msg
    elif cmd.rootCommand == 'set':
        if cmd.targetType == 'data':
            setData(cmd)
        elif cmd.targetType == 'glovar':
            setGlovar(cmd)
        else:
            return False, '----set:unknown'
        msg = '----set:{}:done'.format(cmd.targetType)
        return True, msg
    elif cmd.rootCommand == 'order':
        if cmd.target == 'meths':
            order('methods', cmd)
        elif cmd.target == 'mods':
            order('models', cmd)
        else:
            return False, '----unrecognized target'
        msg = '----order:{}:done'.format(cmd.target)
        return True, msg
    elif cmd.rootCommand == '-help':
        cmd.all == True 
        cmd.helper()
        return True, 'helping'
    else:
        return False, '----command:unrecognized'
    return True, '----PROCESS:DONE----'

if __name__ == "__main__":
    command = None
    if (len(sys.argv) > 0):
        command = Command(sys.argv)
    else:
        msg = 'please, be serious, type a valid command'
        sys.exit(msg)
    command.setCommand()
    res, msg = command.setArgs()
    if res == True:
        print(msg)
    res, msg = switch(command)
    print(msg)

