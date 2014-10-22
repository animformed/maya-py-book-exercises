import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

# define plugin name, used in command registration, so that it can be called in the script editor
kPluginCmdName = "spHelloWorld" # Hence you call this command within the script editor using maya.cmds.spHelloWorld()

# Command class start, derive from MPxCommand
class scriptedCommand(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    # doIt function gets executed when the command is called
    def doIt(self, *args):
        sys.stdout.write("Hello World\n")
# Command class definition ends

# command Creator function
def cmdCreator():
    # returns an instance of the derived command class
    # assigns the ownership to Maya
    return ompx.asMPxPtr(scriptedCommand())

# initialize the script plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        # note how cmdCreator is passed as a reference to a function
        # To register command internally to cmds
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write("Failed to register command %s\n" % kPluginCmdName)
        raise

# Uninitialize the script plugin

def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to register command %s\n" % kPluginCmdName)
        raise
    