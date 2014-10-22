# Objects:
# MDagPath to store camera handle
# MFnCamera to operate on camera
# M3dView class for the Maya views

# Functions:
# M3dView.active3dView() returns M3dView of the active view
# M3dView.getCamera(MDagPath &camera) to get the camera for the view
# doIt(), undoIt(), redoIt(), isUndoable()

# Error trapping:
# Using try/except/else clause instead of MStatus

import sys
import maya.OpenMaya as om
import maya.OpenMayaUI as oui
import maya.OpenMayaMPx as ompx

kPluginCmdName = 'spZoomCamera' # Name of the command, to be used as maya.cmds.spZoomCamera()

# define the command
class scriptedCommand(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)
    
    # to be called later by the doIt()
    def redoIt(self):
        global camera
        fnCamera = om.MFnCamera(camera)
        f1 = fnCamera.focalLength()
        fnCamera.setFocalLength(f1*2.0)
    
    def undoIt(self):
        global camera
        fnCamera = om.MFnCamera(camera)
        f1 = fnCamera.focalLength()
        fnCamera.setFocalLength(f1/2.0)

    def doIt(self, *args):
        global camera
        # create a DAG variable, to obtain a path to the DAG node
        camera = om.MDagPath()
        try:
            # M3dView provides methods for working with 3D model views.
            # active3dView() returns the active view in the form of a class object
            # getCamera() call allocates the DAG path to the input camera
            oui.M3dView.active3dView().getCamera(camera)
        except:
            sys.stderr.write('ERROR: getting camera\n')
        else:
            # will execute if no exception is raised
            self.redoIt()
    
    def isUndoable(self):
        return True
# class definition ends

# Cmd creator
def cmdCreator():    
    return ompx.asMPxPtr(scriptedCommand())

# Initialize the script plug-in
def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)
    try:
        plugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write('Failed to register command: %s\n' % kPluginCmdName)

# Uninitialize the script plug-in
def uninitializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)
    try:
        plugin.deregister(kPluginCmdName)
    except:
        sys.stderr.write('Failed to unregister command: %s' % kPluginCmdName)
        
    