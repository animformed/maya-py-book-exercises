import maya.cmds

# Creating a primitive object
maya.cmds.polySphere(radius= 5)

maya.cmds.polyColorPerVertex(colorRGB = [1, 0, 0], colorDisplayOption = True)

# printing the help for command flags for 'polyCube'
print maya.cmds.help('polyCube')

# Will return a list of string names, the cube transform and creation history node
cubeNodes = maya.cmds.polyCube(name = 'myCube', depth = 4, height = 5, axis = (1, 1, 0))
print cubeNodes

# Editing the value 
maya.cmds.polyCube('myCube1', edit = True, width=10)

# Can only query one thing at a time
h = maya.cmds.polyCube('myCube', query=True, height=True)
print h

sphereNodes = maya.cmds.polySphere()
print sphereNodes

rad = maya.cmds.polySphere('pSphere1', query=True, radius=True)
print rad

maya.cmds.polySphere('pSphere1', edit=True, radius=rad*2)

# As a habit, always capture the names of the nodes created. To avoid naming conflicts, maya might rename them
sphere1 = maya.cmds.polySphere(name='head')
cube1 = maya.cmds.polyCube(name='head')    # named head1
print cube1, sphere1

loc = maya.cmds.spaceLocator()[0]
sx = maya.cmds.getAttr(loc + '.scaleX')
print sx        # print 1.0

sx *= 2    # change sx
maya.cmds.setAttr(loc + '.scaleX', sx) # apply scaleX of 2

# xform is used with transform nodes. Sets the transform values of x, y and z
maya.cmds.xform(loc, translation=[0,1,0])    

# xform can also be used to query values. Here it returns [0.0, 1.0, 0.0]
print maya.cmds.xform(loc, query=True, translation=True)

# getAttr can also be used for this purpose
print maya.cmds.getAttr(loc + '.translate')

# setting the transform values
maya.cmds.setAttr(loc + '.translate', *(1, 2, 3))

# using connectAttr and disconnectAttr
sphere = maya.cmds.polySphere()[0]
cube = maya.cmds.polyCube()[0]
maya.cmds.connectAttr(cube + '.rotateY', sphere + '.translateY')
maya.cmds.select(cube)
# disconnecting
maya.cmds.disconnectAttr(cube + '.rotateY', sphere + '.translateY')

mult = maya.cmds.createNode('multiplyDivide')
maya.cmds.connectAttr(cube + '.rotateY', mult + '.input1X')
maya.cmds.setAttr(mult + '.input2X', 1.0/90.0)
maya.cmds.connectAttr(mult + '.outputX', sphere + '.translateY')
maya.cmds.select(cube)

# Using a dictionary to handle enumerated attributes like rotation order
loc = maya.cmds.spaceLocator()[0]
print maya.cmds.xform(loc, query=True, rotateOrder=True)

print maya.cmds.getAttr('{0}.rotateOrder'.format(loc))    # return '0'
roEnumToStr = {0:'xyz', 1:'yzx', 2:'zxy', 3:'xzy', 4:'yxz', 5:'zyx'}
strToEnumRo = {'xyz':0, 'yzx':1, 'zxy':2, 'xzy':3, 'yxz':4, 'zyx':5}

enumRo = maya.cmds.getAttr('{0}.rotateOrder'.format(loc))    # get the rotate order
print roEnumToStr[enumRo]            # printing the rotate order

# Now setting the rotateOrder
maya.cmds.setAttr('{0}.rotateOrder'.format(loc), strToEnumRo['zxy'])
enumRo = maya.cmds.getAttr('{0}.rotateOrder'.format(loc))    # get the rotate order
print roEnumToStr[enumRo]                   # prints 'zxy'


#Chapter 3
#---------

def process_all_textures():
    print 'Process_all_textures'
    
def process_all_textures(texture_node):
    print 'Processed %s' % texture_node

# Create a file node under Texture in Hypershade
texture = maya.cmds.shadingNode('file', asTexture=True)    

# Run the def with 'texture' as input argument
process_all_textures(texture)            # prints 'Processed file1'

def process_all_textures(**kwargs):
    pre = kwargs.setdefault('prefix', '_my_')
    texture = kwargs.setdefault('texture_node')
    print '%s%s'%(pre, texture)
    
process_all_textures()        # prints '_my_None'
process_all_textures(texture_node='default-jpg')    # prints '_my_default-jpg'

process_all_textures(**dict1)     # Can be used to expand a dictionary into keyword arguments   

# Listing and Selecting Nodes
nodes = maya.cmds.ls()    # store a list of all nodes
print nodes

# store a list of transform nodes
t_nodes = maya.cmds.ls(type = 'transform')
print t_nodes            

# list nodes beginning with 'persp'
nodes = maya.cmds.ls('persp*')    
print nodes

# select nodes beginning with 'side' and 'top'
maya.cmds.select('side*', 'top*')   

# return a list of selected nodes via sl/selection flag
nodes = maya.cmds.ls(sl=True)    
print nodes

# select nodes within the list 'nodes'
maya.cmds.select(nodes)    
import os, maya.cmds, maya.mel

# select all shape nodes
nodes = maya.cmds.ls(type='shape')    
print nodes
# can use ls() with select() to select all shape nodes
maya.cmds.select(maya.cmds.ls(type='shape'))    

# Open a new scene file. Force an action to take place. (new, open, save)
maya.cmds.file(new=True, force=True)

import os
# Create a polyCube
maya.cmds.polyCube()    
# Rename the file as C:/Users/localhost/Documents/cube.ma
maya.cmds.file(rename = os.path.join(os.getenv('HOME'), 'cube.ma'))
# Now save the file
maya.cmds.file(save=True)
# Open a new scene
maya.cmds.file(new=True, force=True)
# Load the 'cube.ma' scene
maya.cmds.file(os.path.join(os.getenv('HOME'), 'cube.ma'), open=True, force=True)


# The following lines open a new scene, create a sphere named “Earth”, and add a mass attribute to its transform node.
maya.cmds.file(new=True, force=True)
sphere_transform = maya.cmds.polySphere(name='Earth')[0]
maya.cmds.addAttr(sphere_transform, attributeType='float', shortName='mass', longName='mass', defaultValue=5.9742e24)
# Getting the value of the new attribute. Returns '5.9742000056604751e+24'
maya.cmds.getAttr(sphere_transform + '.mass')
# Add a new string attribute to the transform
maya.cmds.addAttr(sphere_transform, dataType='string', shortName='alt', longName='alternateName')

# process_all_textures() searches for a texture_nodes keyword. It will iterate through all of the items in 
# the collection specified with this keyword, rename them all, and append them to a new_texture_names list 
# to return.
def process_all_textures(**kwargs):
    # get or create key 'prefix' with value 'my_'. Returns 'dirt_'
    pre = kwargs.setdefault('prefix', 'my_')
    # get file list from key 'texture_nodes'. Returns '[u'file1', u'file2', u'file3']'
    textures = kwargs.setdefault('texture_nodes')
    new_textures_names = []
    if isinstance(textures, list) or isinstance(textures, tuple):
        for texture in textures:
            # Append the new renamed 'file' nodes with prefix 'dirt_'
            new_textures_names.append(maya.cmds.rename(texture, '%s%s' % (pre, texture)))
        return new_textures_names
    else:
        maya.cmds.error('No texture nodes specified')
# Now, create a new scene   
maya.cmds.file(new=True, f=True)
textures = []
# Create 3 'file' nodes in hypershade as textures
for i in range(3):
    textures.append(maya.cmds.shadingNode('file', asTexture=True))
# Run the def process_all_textures. Get the renamed 'file' list. Print the result.
new_textures = process_all_textures(texture_nodes = textures, prefix='dirt_')
print new_textures

# Get all transform nodes
xform_list = maya.cmds.ls(type='transform')
camera_name = 'persp'
# If the 'persp' exists in the transforms list, print the result
if(isinstance(xform_list, list) and camera_name in xform_list):
    print camera_name, 'is in the list of the transforms'

# Modify process_all_textures() to chekc whether the input prefix argument contains an 
# underscore suffix. If not, it adds it.
def process_all_textures(**kwargs):
    pre = kwargs.setdefault('prefix')
    if isinstance(pre, str) or isinstance(pre, unicode):
        # Now check is the last element in pre is an underscore. If not add a '_'.
        if not pre[-1] == '_':
            pre += '_'
    textures = kwargs.setdefault('texture_nodes')
    new_textures_names = []
    if isinstance(textures, list) or isinstance(textures, tuple):
        for texture in textures:
                # Append the new renamed 'file' nodes with prefix 'dirt_'
                new_textures_names.append(maya.cmds.rename(texture, '%s%s' % (pre, texture)))
        return new_textures_names
    else:
        maya.cmds.error('No texture nodes specified')

tex = [maya.cmds.shadingNode('file', asTexture=True)]
print 'Before:', tex
tex = process_all_textures(prefix='metal', texture_nodes=tex) 
print 'After:', tex

def process_all_textures(**kwargs):
    pre = kwargs.setdefault('prefix')
    if isinstance(pre, str) or isinstance(pre, unicode):
        if not pre[-1] == '_':
            pre += '_'
    textures = kwargs.setdefault('texture_nodes')
    new_texture_names = []
    if isinstance(textures, list) or isinstance(textures, tuple):
        for texture in textures:
            # if the texture not found or is not a file texture, break
            if maya.cmds.ls(texture) and maya.cmds.nodeType(texture) == 'file':
                new_texture_names.append(maya.cmds.rename(texture, pre+texture))
        return new_texture_names
    else:
        # raise TypeError, 'Argument passed was not a list or a tuple'
        maya.cmds.error('No texture nodes specified')
        
new_textures = ['nothing', 'persp', maya.cmds.shadingNode('file', asTexture=True)]     
print 'Before:', new_textures        # prints '['nothing', 'persp', u'file8']'
new_textures = process_all_textures(prefix='concrete', texture_nodes=new_textures)  
print 'After:', new_textures         # prints '[u'concrete_file8']'

texture_list = ['rock_diff', 'base_diff', 'base_spec', 'grass_diff', 'grass_bump']
diff_list = []
for texture in texture_list:
    if '_diff' in texture:
        diff_list.append(texture)
print diff_list        # prints '['rock_diff', 'base_diff', 'grass_diff']'

diff_list = [texture for texture in texture_list if texture.endswith('_diff')]    # alternate method, give same result
    
def process_all_textures(out_dir = os.getenv('HOME')):
    """
    A function that gets a list of textures from the current scene and 
    processed each texture according to name
    """
    texture_nodes = []        # to be replaced
    processed_textures = []
    error_textures = []
    skipped_textures = []
    
    if not texture_nodes:
        maya.cmds.warning('No textures found, exiting')
        return (processed_textures, error_textures, skipped_textures)
    if is_valid_texture(name):
        print 'Processing texture', name
        as_type = None
        status = False
        texture = None
    if '_diff' in name:
        status, texture = process_diffuse(name, out_dir)
    if status:
        processed_textures.append(texture)
        as_type = 'diffuse'
    else:
        error_textures.append(texture)
    elif '_spec' in name:
        status, texture = process_spec(name, out_dir)
    if status:
        processed_textures.append(texture)
        as_type = 'specular'
    else:
        error_textures.append(texture)
    elif '_bump' in name:
        status, texture = process_bump(name, out_dir)
    if status:
        processed_textures.append(texture)
        as_type = 'bump'
    else:
        error_textures.append(texture)
    if status:
        print 'Processed %s as a %s texture' % (texture, as_type)
    else:
        print 'Failed to process', name
    else:
        print '%s is not a valid texture, skipping.' % name
        skipped_textures.append(name)
        return (processed_textures, error_textures, skipped_textures)