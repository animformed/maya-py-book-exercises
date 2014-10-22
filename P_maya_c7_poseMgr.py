import maya.cmds as cmds
import maya.mel as mel
import os, cPickle, sys, time, pprint

kPoseFileExtension = 'pse'

def showUI():
    """
    A function to instantiate the pose manager window
    """
    return AR_PoseManagerWindow.showUI()

class AR_PoseManagerWindow(object):
    """
    A class for a basic pose manager window
    """
    @classmethod
    def showUI(cls):
        """
        A function to instantiate the pose manager window
        """
        # Create an instance
        win = cls()
        # create a window
        win.create()
        # return the instance
        return win
    
    def __init__(self):
        """
        Initialize data attributes
        """
        # a unique window handle
        self.window = 'ar_poseManagerWindow'
        # window title
        self.title = 'Pose Manager'
        # window size
        self.size = (300, 174)
        if mel.eval('getApplicationVersionAsFloat()') > 2010.0:
            self.size = (300, 150)
        # a temporary file in a writable location for storing a copied pose
        # os.path.expanduser('~') returns C:\\Users\\localhost', it expands ~ and ~user constructs;
        # likewise, os.path.expanduser('~user') returns C:\\Users\\user',
        self.tempFile = os.path.join(os.path.expanduser('~'), 'temp_pose.%s' % kPoseFileExtension)
        # current clipboard status message
        self.clipboardStat = 'No pose currently copied.'
        if (os.path.exists(self.tempFile)):
            self.clipboardStat = 'Old pose currently copied to clipboard.'
        # file filter to display in file browsers
        self.fileFilter = 'Pose (*.%s)' % kPoseFileExtension
    
    def create(self):
        """
        Draw the window
        """
        # delete the window if its handle exists
        if(cmds.window(self.window, exists=True)):
            cmds.deleteUI(self.window, window=True)
        # initialize the window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size, sizeable=False)
        # main form layout
        self.mainForm = cmds.formLayout()
        # frameLayout below window for copy and paste poses
        self.copyPasteFrame = cmds.frameLayout(label='Copy and Paste Poses')
        # formLayout inside of frame
        self.copyPasteForm = cmds.formLayout()
        # create buttons in a 2-column grid
        self.copyPasteGrid = cmds.gridLayout(cellWidth=(self.size[0]/2)-2, numberOfColumns=2)
        # create two buttons for copy and paste
        self.copyBtn = cmds.button(label='Copy Pose', command=self.copyBtnCmd)
        self.pasteBtn = cmds.button(label='Paste Pose', command=self.pasteBtnCmd)
        # set parent to self.copyPasteForm
        cmds.setParent(self.copyPasteForm)
        # scroll view with label for clipboard status
        self.clipboardLayout = cmds.scrollLayout(height=42, width=self.size[0]-4)
        self.clipboardLb = cmds.text(label=self.clipboardStat)
        # attach controls in the copyPaste form
        at_c = []; at_f = []
        at_c.append([self.clipboardLayout, 'top', 0, self.copyPasteGrid])
        at_f.append([self.copyPasteGrid, 'top', 0])
        at_f.append([self.clipboardLayout, 'bottom', 0])
        cmds.formLayout(self.copyPasteForm, edit=True, attachControl= at_c, attachForm=at_f)
        # set parent to self.mainForm
        cmds.setParent(self.mainForm)
        # frameLayout for saving and loading poses
        self.loadSaveFrame = cmds.frameLayout(label='Save and load Poses')
        # create buttons in a 2-column grid
        self.loadSaveBtnLayout = cmds.gridLayout(cellWidth=(self.size[0]/2)-2, numberOfColumns=2)
        self.saveBtn = cmds.button(label='Save Pose', command=self.saveBtnCmd)
        self.loadBtn = cmds.button(label='Load Pose', command=self.loadBtnCmd)
        # now attach frames to self.mainForm
        at_c = []; at_f = []
        at_c.append([self.loadSaveFrame, 'top', 0, self.copyPasteFrame])
        at_f.append([self.copyPasteFrame, 'top', 0])
        at_f.append([self.copyPasteFrame, 'left', 0])
        at_f.append([self.copyPasteFrame, 'right', 0])
        at_f.append([self.loadSaveFrame, 'bottom', 0])
        at_f.append([self.loadSaveFrame, 'left', 0])
        at_f.append([self.loadSaveFrame, 'right', 0])
        cmds.formLayout(self.mainForm, edit=True, attachControl=at_c,attachForm=at_f)
        # show the window
        cmds.showWindow(self.window)
        
    def getSelection(self):
        """
        Get current selection, and check if it's a transform
        """
        rootNodes = cmds.ls(selection=True, type='transform')
        #for node in rootNodes:
        #    nt = cmds.nodeType(node)
        #    if nt == 'transform' or nt == 'joint':
        #        res.append(node)
        if rootNodes is None or len(rootNodes) < 1:
            cmds.confirmDialog(title='Error', message='Please select one or more transform nodes.', button='OK')
            return None
        return rootNodes
    
    def copyBtnCmd(self, *args):
        """
        Called when the Copy Pose button is pressed
        """
        rootNodes = self.getSelection()
        if rootNodes is None:
            return
        # edit the label text for clipboard status
        cmds.text(self.clipboardLb, edit=True, label='Pose copied at %s for %s.' %
                                # representing time in a str format. %I-(Hour in decimal in 12-hour clock)
                                # %M-(Minute as a decimal number
                                (time.strftime('%I:%M'),
                                # join transform names with commas as a single unicode or str
                                ', '.join(rootNodes)))
        # export the pose of selected transforms to the self.tempFile
        self.exportPose(self.tempFile, rootNodes)
    
    def pasteBtnCmd(self, *args):
        """
        Called when the Paste Pose button is pressed
        """
        if not os.path.exists(self.tempFile):
            return
        self.importPose(self.tempFile)
    
    def saveBtnCmd(self, *args):
        """
        Called when the Save Pose button is pressed
        """
        rootNodes = self.getSelection()
        if rootNodes is None:
            return
        # get the file path using fileDialog
        # Maya 2011 and newer use fileDialog2
        try:
            filePath = cmds.fileDialog2(fileFilter=self.fileFilter, fileMode=0)
        # BUG: Maya 2008 and older may, on some versions of OS X, return the
        # path with no separator between the directory and file names:
        # e.g., /users/adam/Desktopuntitled.pse 
        except:
            filePath = cmds.fileDialog(directoryMask='*.%s' % kPoseFileExtension, mode=1)
        # early out of the dialog was cancelled
        if filePath is None or len(filePath) < 1:
            return
        if isinstance(filePath, list):
            filePath = filePath[0]
            self.exportPose(filePath, self.getSelection())
    
    def loadBtnCmd(self, *args):
        """
        Called when the Load Pose Button is pressed
        """
        # Maya 2011 and newer use fileDialog2
        try:
            filePath = cmds.fileDialog2(fileFilter=self.fileFilter, fileMode=1)
        except:
            filePath = cmds.fileDialog(directoryMask='*.%s' % kPoseFileExtension, mode=0)
        # early out of the dialog was cancelled
        if filePath is None or len(filePath) < 1:
            return
        if isinstance(filePath, list):
            filePath = filePath[0]
            self.importPose(filePath)
    
    def exportPose(self, filePath, rootNodes):      
        """
        Save a pose file at filePath for rootNodes and their children
        """
        print filePath
        print rootNodes 
        # try to open the file
        try:
            f = open(filePath, 'w')
        except IOError:
            cmds.confirmDialog(title='Error', button='OK', message='Unable to write file: %s' % filePath)
            raise
        # built a list of hierarchy data
        data = self.saveHierarchy(rootNodes, {})
        # pickle the serialized data
        cPickle.dump(data, f)
        # close the file
        f.close()
    
    def saveHierarchy(self, rootNodes, data):
        """
        Append attribute values for all keyable attributes to data array
        """
        # iterate through supplied nodes
        for node in rootNodes:
            keyableAttrs = cmds.listAttr(node, keyable=True)
            if keyableAttrs:
                for attr in keyableAttrs:
                    data[node] = data.get(node, []) + [[attr, cmds.getAttr('%s.%s'%(node,attr))]]
            # if there are children, repeat
            children = cmds.listRelatives(node, children=True)
            if children:
                self.saveHierarchy(children, data)
        return data
    
    def importPose(self, filePath):
        """
        Import the pose data stored in filePath
        """
        # try to open the file
        try:
            f = open(filePath, 'r')
        except IOError:
            cmds.confirmDialog(title='Error', button='OK', message='Unable to open file: %s' % filePath)
            raise
        # unpickle the data
        data = cPickle.load(f)
        # close the file
        f.close()
        # set the attributes for stored pose
        errAttrs = {}
        for node in data:
            for attr in data[node]:
                try:
                    cmds.setAttr('%s.%s' % (node, attr[0]), attr[-1])
                except:
                    errAttrs[node] = errAttrs.get(node, []) + [[attr[0], attr[-1]]]
        # display error message if needed
        if len(errAttrs) > 0:
            self.importErrorWindow(errAttrs)
            sys.stderr.write('Not all attributes could be loaded.')
            #cmds.warning("Not all attributes could be loaded.")
    
    def importErrorWindow(self, errAttrs):
        """
        An error window to display if there are unknown attributes when importing a pose
        """
        win = 'ar_errorWindow'
        # kill the window if it exists
        if cmds.window(win, exists=True):
            cmds.deleteUI(win, window=True)
        # create the window
        cmds.window(win, title='Unknown Attributes', widthHeight=(300, 200), sizeable=False)
        # create a formLayout for window
        errorForm = cmds.formLayout()
        # info label
        infoLb = cmds.text(label='The following attributes can\'t be found.'
                            '\nThey\'re being ignored.', align='left')
        # display a list of attributes that could not be loaded
        scroller = cmds.scrollLayout(width=300)
        errStr = ''
        for node in errAttrs:
            for item in errAttrs[node]:
                errStr += '{0:<15}-({1:<15}:{2:.2f})\n'.format(str(node), item[0], item[-1])
        # create a text control inside scrollLayout
        cmds.text(label=errStr, align='left')
        # create a button to dismiss the window
        btn = cmds.button(label='OK', parent=errorForm, height=26, command=cmds.deleteUI(win, window=True))
        # attach controls
        cmds.formLayout(errorForm, edit=True, attachControl=
                        ([scroller, 'top', 5, infoLb],
                         [scroller, 'bottom', 5, btn]),
                        attachForm=
                        ([infoLb, 'top', 5],
                         [infoLb, 'left', 5],
                         [infoLb, 'right', 5],
                         [scroller, 'left', 0],
                         [scroller, 'right', 0],
                         [btn, 'left', 5],
                         [btn, 'right', 5],
                         [btn, 'bottom', 5]))
        # show the window
        cmds.showWindow(win)