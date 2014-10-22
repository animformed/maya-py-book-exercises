import maya.cmds as cmds

class AR_OptionsWindow(object):
    """
    A base class for an options window.
    """
    @classmethod
    # To retain information per class
    def showUI(cls):
        """
        A function to instantiate the options window
        """
        # Create an instance
        win = cls()
        # create a window
        win.create()
        # return the instance
        return win
    
    def __init__(self):
        """
        Initialize common data attributes
        """
        # unique window handle
        self.window = 'ar_optionsWindow'
        # window title
        self.title = 'Options Window'
        # window size
        self.size = (546, 350)
        # specify whether the tool/action toggle is supported
        self.supportsToolAction = True
        # name to display on the action button
        self.actionName = 'Apply and Close'
    
    def create(self):
        """
        Draw the window
        """
        # delete the window if its handle exists
        if cmds.window(self.window, exists=True):
            # deletes window. 'window' flag makes sure that deleted object is a window
            cmds.deleteUI(self.window, window=True)
        # initialize the window
        self.window = cmds.window(title=self.title, widthHeight=self.size, menuBar=True) 
        # main form for the window
        self.mainForm = cmds.formLayout(numberOfDivisions=100)
        # create common menu items items and buttons
        self.commonMenu()
        self.commonButtons()
        # create a tabLayout
        self.optionsBorder = cmds.tabLayout(scrollable=True, tabsVisible=False, height=1)
        # Attach tabLayout to parent formLayout, and to control button
        cmds.formLayout(self.mainForm, edit=True, attachForm=
                        ([self.optionsBorder, 'top', 0],
                        [self.optionsBorder, 'left', 2],
                        [self.optionsBorder, 'right', 2]),
                        attachControl=
                        ([self.optionsBorder, 'bottom', 5, self.applyBtn]))
        # new form to attach controls in displayOptions()
        self.optionForm = cmds.formLayout(numberOfDivisions=100)
        self.displayOptions()
        # Show the window
        cmds.showWindow(self.window)
    
    def commonMenu(self):
        """
        Create common menu items for all option boxes
        """
        # create a menu, which comes below formLayout
        self.editMenu = cmds.menu(label='Edit')
        # create menuItem(s), after menu
        self.editMenuSave = cmds.menuItem(label='Save Settings', command=self.editMenuSaveCmd)
        # since command flag is not a return placeholder, but to point to a callback function; so we can't use func(). 
        # We can also use partial() from functools module to point to callback function, and pass arguments as well.
        # So this will be command=functools.partial(self.editMenuSaveCmd, *args)
        self.editMenuReset = cmds.menuItem(label='Reset Settings', command=self.editMenuResetCmd)
        self.editMenuDiv = cmds.menuItem(divider=True)
        # create a radio menu item collection
        self.editMenuRadio = cmds.radioMenuItemCollection()
        self.editMenuTool = cmds.menuItem(label='As Tool', radioButton=True, 
                                          enable=self.supportsToolAction, 
                                          command=self.editMenuToolCmd)
        self.editMenuAction = cmds.menuItem(label='As Action', radioButton=True, 
                                            enable=self.supportsToolAction, 
                                            command=self.editMenuActionCmd)
        # will create a help on menuBar
        self.helpMenu = cmds.menu(label='Help')
        self.helpMenuItem = cmds.menuItem(label='Help on %s' % self.title, command=self.helpMenuCmd)
        
    def commonButtons(self):
        """
        Create common buttons for all option boxes
        """
        self.commonBtnSize = ((self.size[0]-18)/3, 26)
        # The basic idea for computing the width is that we want 5 pixels of padding on the left and right, 
        # and 4 pixels of padding in between the buttons (5+4+4+45 =18). Hence, we subtract a total of 
        # 18 from the window's width before dividing by 3. The height is 26 pixels.
        self.actionBtn = cmds.button(label=self.actionName, height=self.commonBtnSize[1],
                                     command=self.actionBtnCmd)
        self.applyBtn = cmds.button(label='Apply', height=self.commonBtnSize[1],
                                     command=self.applyBtnCmd)
        self.closeBtn = cmds.button(label='Close', height=self.commonBtnSize[1],
                                     command=self.closeBtnCmd)
        cmds.formLayout(self.mainForm, edit=True, attachForm=
                        ([self.actionBtn, 'left', 5],
                        [self.actionBtn, 'bottom', 5],
                        [self.applyBtn, 'bottom', 5],
                        [self.closeBtn, 'bottom', 5],
                        [self.closeBtn, 'right', 5]),
                        attachPosition=
                        ([self.actionBtn, 'right', 1, 33],
                         [self.closeBtn, 'left', 0, 67]),
                        attachControl=
                        ([self.applyBtn, 'left', 4, self.actionBtn],
                         [self.applyBtn, 'right', 4, self.closeBtn]),
                        attachNone=
                        ([self.actionBtn, 'top'],
                         [self.applyBtn, 'top'],
                         [self.closeBtn, 'top']))
                         
    def displayOptions(self):
        """
        Override this method to display options controls
        """
        pass
                        
    def helpMenuCmd(self, *args):
        """
        Override this method to display custom help
        """
        cmds.launch(web='http://maya-python.com')
    
    def editMenuSaveCmd(self, *args):
        """
        Override this method to implement Save Settings
        """
        pass
    
    def editMenuResetCmd(self, *args):
        """
        Override this method to implement Reset Settings
        """
        pass
    
    def editMenuToolCmd(self, *args):
        """
        Override this method to implement tool mode
        """
        pass
    
    def editMenuActionCmd(self, *args): 
        """
        Override this method to implement action mode
        """
        pass
    
    def actionBtnCmd(self, *args):
        """
        Apply actions and close window
        """
        pass
    
    def applyBtnCmd(self, *args):
        """
        Override this method to apply actions
        """
        pass
    
    def closeBtnCmd(self, *args):
        """
        Close Window
        """
        cmds.deleteUI(self.window, window=True)
