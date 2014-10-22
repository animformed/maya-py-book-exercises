import maya.cmds
import math

pi = math.pi

def getCircumference(obj):
    try:
        return maya.cmds.getAttr(obj + '.radius') * 2 * pi
    except:
        raise
def getHeight(obj):
    try:
        return maya.cmds.getAttr(obj + '.height')
    except:
        raise

# Now in maya, type the following

#import m_primitives.P_maya_c4_create as mc
#import m_primitives.P_maya_c4_math as mm
#cyl = mc.cylinder(r=0.25)
#print 'Circumference is %.3f' % mm.getCircumference(cyl)    # prints 'Circumference is 1.571'   