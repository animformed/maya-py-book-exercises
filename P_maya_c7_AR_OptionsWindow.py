import maya.cmds as cmds
class AR_OptionsWindow(object):
    def __init__(self):
        self.window = 'ar_optionsWindow'
        self.title = 'Options Window'
        self.size = (546, 350)
        self.supportsToolAction = False
        
    def create(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.showWindow()
    
    def commonMenu(self):
        self.editMenu = cmds.menu(label='Edit')
        self.editMenuSave = cmds.menuItem(label='Save Settings')
        self.editMenuReset = cmds.menuItem(label='Reset Settings')
        self.editMenuDiv = cmds.menuItem(d=True)
        self.editMenuRadio = cmds.radioMenuItemCollection()
        self.editMenuTool = cmds.menuItem(label='As Tool', radioButton=True, enable=self.supportsToolAction)
        self.editMenuAction = cmds.menuItem(label='As Action', radioButton=True, enable=self.supportsToolAction)
        self.helpMenu = cmds.menu(label='Help')
        self.helpMenuItem = cmds.menuItem(label='Help on %s' % self.title)