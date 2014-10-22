import maya.cmds as cmds
from P_maya_c7_poseMgr import *

# create an instance
pwin = AR_PoseManagerWindow()
# create the window
pwin.create()
# toggle the visibility of the window (self.window) here when using docking
cmds.toggleWindowVisibility(pwin.window)
# add a pane for docking
layout1 = cmds.paneLayout(configuration='single')
# add dockControl
dock = cmds.dockControl(label=pwin.title, width=pwin.size[0], allowedArea='all', area='right', floating=False, content=layout1)
cmds.control(pwin.window, edit=True, parent=layout1)