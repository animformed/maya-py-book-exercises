import maya.cmds as cmds
from P_maya_c7_OptionWin import AR_OptionsWindow

class AR_PolyOptionsWindow(AR_OptionsWindow):
    """A class for a simple window to create polygon primitives"""
    def __init__(self):
        """
        Initialize base class and override data attributes
        """
        AR_OptionsWindow.__init__(self)
                # overridden from base class
        self.title = 'Polygon Creation Options'
        self.actionName = 'Create'

    def displayOptions(self):
            """
            Overridden from base class
            """
            # primitive type selector
            self.objType = cmds.radioButtonGrp(label='Object Type: ', 
                                               labelArray4=['Cube', 'Cone', 'Cylinder', 'Sphere'],
                                               numberOfRadioButtons=4,
                                               select=1) # selected radio button
            # a group of transform controls. Create a frameLayout to hold the controls
            self.xformGrp = cmds.frameLayout(label='Transformations', collapsable=True)
            # self.optionForm (empty formLayout) is from superclass
            cmds.formLayout(self.optionForm, edit=True, attachControl=
                            # attach the formLayout below radio buttons
                            ([self.xformGrp, 'top', 2, self.objType]),
                            attachForm=
                            ([self.xformGrp, 'left', 0],
                             [self.xformGrp, 'right', 0]))
            # create a columnLayout below formLayout. Placing too many children under
            # self.xformGrp would throw an exception in maya versions before 2011.
            self.xformCol = cmds.columnLayout()
            # create floatFieldGrp for translate, rotate and scale transform
            self.position = cmds.floatFieldGrp(label='Position: ', numberOfFields=3)
            self.rotation = cmds.floatFieldGrp(label='Rotation (XYZ): ', numberOfFields=3)
            self.scale = cmds.floatFieldGrp(label='Scale: ', numberOfFields=3,
                                            value=[1.0, 1.0, 1.0, 1.0])

            # parent is set to self.xformGrp
            cmds.setParent('..')
            # parent is set to self.optionForm
            cmds.setParent('..')

            # a vertex color picker under self.optionForm
            self.color = cmds.colorSliderGrp(label='Vertex Colors: ')
            # edit the placement of self.color under self.optionForm
            cmds.formLayout(self.optionForm, edit=True, attachControl=
                            ([self.color, 'top', 0, self.xformGrp]),
                                                         attachForm=
                                                         ([self.color, 'left', 0]))

    def applyBtnCmd(self, *args):
            """
            Overridden from base class
            """
            # determine the type of object to create from radio button index
            self.objIndAsCmd = {1:cmds.polyCube, 2:cmds.polyCone, 
                                3:cmds.polyCylinder, 4:cmds.polySphere}
            # determine the selected radio button from radioButtonGrp self.objType
            objIndex = cmds.radioButtonGrp(self.objType, query=True, select=True)
            # create the selected new poly object
            newObject = self.objIndAsCmd[objIndex]()
            # From this point, you can apply transformation using the float field
            # in an absolute (relative to parent) or as initial transformation at creation

            # Absolute transformation
            # Connecting the translates
            # index 1 is the label, so it begins from index=2
            cmds.connectControl(self.position, '%s.translateX' % newObject[0], index=2) 
            cmds.connectControl(self.position, '%s.translateY' % newObject[0], index=3)
            cmds.connectControl(self.position, '%s.translateZ' % newObject[0], index=4)
            # Connecting the rotations
            cmds.connectControl(self.rotation, '%s.rotateX' % newObject[0], index=2) 
            cmds.connectControl(self.rotation, '%s.rotateY' % newObject[0], index=3)
            cmds.connectControl(self.rotation, '%s.rotateZ' % newObject[0], index=4)
            # Connecting the scales
            cmds.connectControl(self.scale, '%s.scaleX' % newObject[0], index=2) 
            cmds.connectControl(self.scale, '%s.scaleY' % newObject[0], index=3)
            cmds.connectControl(self.scale, '%s.scaleZ' % newObject[0], index=4)
            
            # Initial transformation
#            # Query the values from the fields
#            pos = cmds.floatFieldGrp(self.position, query=True, value=True)
#            rot = cmds.floatFieldGrp(self.rotation, query=True, value=True)
#            scale = cmds.floatFieldGrp(self.scale, query=True, value=True)
#            # apply the transformation
#            cmds.xform(newObject[0], translation=pos, rotation=rot, scale=scale)
            
            # apply vertex colours to the new object, from the color picker of 
            # colorSliderGrp, self.color
            # First, query the colour from self.color
            col = cmds.colorSliderGrp(self.color, query=True, rgbValue=True)
            # Then apply the color to the new object. 
            cmds.polyColorPerVertex(newObject[0], colorRGB=col, 
                                    # enable the mesh to display vertex colors
                                    colorDisplayOption=True)