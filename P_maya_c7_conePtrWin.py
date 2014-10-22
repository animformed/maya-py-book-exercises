import maya.cmds as cmds
import os

class AR_QtConePtrWindow(object):
    """
    A class for a window to create a cone pointing in a direction
    """
    use = None
    
    @classmethod
    def showUI(cls):
        """
        A function to instantiate the window
        """
        win = cls(uiFile)
        win.create()
        return win
    
    def __init__(self, filePath):
        """
        Initialize data attributes
        """
        # allow controls to initialize using class attributes.
        # When you're assigning dynamic properties (using Qt ui), you can't call a class 
        # attribute(method) as a bound method directly. When maya builds the UI (Qt ui), even
        # when it is loaded from inside a class, its controls are not constructed in the
        # context of the instance object, where the self name exists, but in __main__. 
        AR_QtConePtrWindow.use = self
        # unique window handle
        self.window = 'ar_conePtrWindow'
        # name of the rotation input field
        self.rotField = 'inputRotation'
        # the path to the .ui file
        self.uiFile = filePath
    
    def create(self, verbose=False):
        """
        Draw the window pane
        """
        # delete the window if its handle exists
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)
        # initialize the window as a pane for docking
        self.window = cmds.loadUI(uiFile=self.uiFile, verbose=verbose)
        #layoutWin = cmds.paneLayout(configuration='single')
        # create a dockControl and parent the control to layoutWin
        cmds.dockControl(allowedArea='all', area='right', floating=False, 
                         height=cmds.window(self.window, query=True, height=True), 
                         content=self.window, label='Docked Cone Pointer Window')
        cmds.showWindow(self.window)
           
    def createBtnCmd(self, *args):
        """
        Function to execute when create button is pressed
        """
        self.cone = cmds.polyCone()
        cmds.setAttr('%s.rotateX' % self.cone[0], 90)
    
    def rotateCone(self, *args):
        """
        Rotate the cone
        """
        rotation = '|'.join([self.window, 'centralwidget','spinbox','value'])
        rotation = cmds.textField(rotation, query=True, text=True) 
        print rotation
        #cmds.rotate(0, rot, 0, self.cone[0], relative=True)