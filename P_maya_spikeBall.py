"""
This script prints some information and creates a spike ball
"""
import maya.cmds

def addSpikes(obj):
    """
    This function adds spikes to a polygon object.
    """
    try:
        # Return the number of faces
        polycount = maya.cmds.polyEvaluate(obj, face=True)
    except:
        raise
    # Iterate through faces
    for i in range(0, polycount):
        face = '{0}.f[{1}]'.format(obj, i)
        # Extrude face individually, pass the face as argument. Adjust the Z translate and scale the face.
        maya.cmds.polyExtrudeFacet(face, localTranslateZ=1, ch=0)
        maya.cmds.polyExtrudeFacet(face, localTranslateZ=1, ch=0, localScale=[0.1, 0.1, 0.1])
    # Smooth the normals. Specifying a smoothing angle
    maya.cmds.polySoftEdge(obj, angle=180, ch=0)
    # Select the transform
    maya.cmds.select(obj)
print 'module name:', __name__
print 'globals:'
for k in globals().keys():
    print '\t%s' % k

# Create a pSolid primitive without construction history, pass the transform as the argument
addSpikes(maya.cmds.polyPrimitive(ch=0)[0])