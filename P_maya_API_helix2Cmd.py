# Turns a selected nurbs curve to a helix.

# Classes:
# MPxCommand revisited
# MSyntax is used to specify flags and arguments passed to commands
# MArgDatabase parses argument lists based on a syntax object
# MSyntax which describes the format for a command
# MItSelectionList: Iterator of MSelectionList, allows filtering
# MSelectionList: A list of MObjects
# MFnNurbsCurve
# MPointArray, MDoubleArray, MPoint
# MItCurveCV
# MDagPath
# MGlobal

# Important Functions: 
# MGlobal.getActiveSelectionList() - To retrieve the selected curve 
# syntaxCreator() - To create the syntax object MSyntax based on the flags
# registerCommand revisited - add a third parameter, which is a reference to the syntax creator function

# Key points:
# MPxCommand.syntax() is intended to be used in an MArgDatabase constructor when the plugin
# command's syntax is being initialized. 

# The user should declare and define a syntax creator function that must be registered with Maya
# by passing the function reference as a parameter in MFnPlugin::registerCommand()

# When MPxCommand.syntax() is called it returns the syntax object that the user has created
# in the custom syntax constructing method that was registered.

# To avoid conflicts the user's syntax defining function must be given a name other than 'syntax'.

import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import sys, math

kPluginCmdName = 'spHelix2'

# Define command line flags, they will be used later in the syntax creator function. You have to
# define short and long format of the flag
kPitchFlag = '-p'
kPitchLongFlag = '-pitch'
kRadiusFlag = '-r'
kRadiusLongFlag = '-radius'

class scriptedCommand(ompx.MPxCommand):
    def __init__(self):
        # call the constuctor of the MPxCommand
        ompx.MPxCommand.__init__(self)
        
        # define instance variables
        # DagPath to point to selected curve
        self.fDagPath = om.MDagPath()
        # Array to store CV coordinates, array of MPoint(s)
        self.fCVs = om.MPointArray()
        # default values of radius and pitch
        self.radius = 4.0
        self.pitch = 0.5
        
    def doIt(self, args):
        # parse the arguments
        # self.syntax() is the MPxCommand method we talked about earlier
        argData = om.MArgDatabase(self.syntax(), args)
        if argData.isFlagSet(kPitchFlag):
            self.pitch = argData.flagArgumentDouble(kPitchFlag, 0)
        
        if argData.isFlagSet(kRadiusFlag):
            self.radius = argData.flagArgumentDouble(kRadiusFlag, 0)
        
        # instantiate MSelectionList to store active selections
        slist = om.MSelectionList()
        
        # assign active list to slist
        om.MGlobal.getActiveSelectionList(slist)
        
        # retrieve only NurbsCurves. Filter selection
        i_list = om.MItSelectionList(slist, om.MFn.kNurbsCurve)
        if i_list.isDone():
            sys.stderr.write('Error: No curve selected\n')
            return
        
        # retrieve the dag path of the current selection item, and store it in the in 
        # the instance variable self.fDagPath
        i_list.getDagPath(self.fDagPath)
        self.redoIt()
    
    def redoIt(self):
        # create a function set to operate on the curve pointed to by MDagPath
        curveFn = om.MFnNurbsCurve(self.fDagPath)
        
        # get number of CVs
        numCVs = curveFn.numCVs()
        
        # retrieve the CVs and store them in the CVs array
        curveFn.getCVs(self.fCVs)
        sys.stdout.write('numCVs: %s\n' % numCVs)
        
        # copy the CVs to another MPointArray, which will be used to construct the helix
        points = om.MPointArray(self.fCVs)
        
        # calculate the coordinates of the helix CVs
        for i in range(0, numCVs):
            points.set(i, self.radius * math.cos(i), self.pitch * i, self.radius * math.sin(i))
        
        # Set CV at the given index to the given point.
        # The method updateCurve should be called to trigger changes in the curve
        curveFn.setCVs(points)
        curveFn.updateCurve()
    
    def undoIt(self):
        curveFn = om.MFnNurbsCurve(self.fDagPath)
        
        # update the curve with the original values of the CVs
        curveFn.setCVs(self.fCVs)
        curveFn.updateCurve()
        self.fCVs.clear()
        
    def isUndoable(self):
        return True
    
    # destructor to clear the list of CVs. Saves memory
    def __del__(self):
        self.fCVs.clear()
# class definition ends

# Creator
def cmdCreator():
    # Change ownership to maya
    return ompx.asMPxPtr(scriptedCommand())

# Syntax creator
def syntaxCreator():
    # create the syntax object
    syntax = om.MSyntax()
    # add the flags short form, long form and data type. First for the Pitch, and then radius
    syntax.addFlag(kPitchFlag, kPitchLongFlag, om.MSyntax.kDouble)
    syntax.addFlag(kRadiusFlag, kRadiusLongFlag, om.MSyntax.kDouble)
    return syntax

# Initialize the script plugin
def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject, 'BlaBla', '2008', 'whatever')
    try:
        # a third argument was added. A reference to the syntax creator
        mplugin.registerCommand(kPluginCmdName, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command helix')
        raise

# uninitialize plugin
def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command helix')
        raise

    
    
        
            
            

