import os
import maya.cmds
import maya.mel

def process_all_textures(out_dir = os.getenv('HOME'), new_file = 'processed.ma'):
    """
    A function that gets a list of textures from the current scene
    and processes each texture according to name
    
    out_dir = Home directory (string)
    new_file = Name of the scene file (string)
    """
    # create a list of valid file texture nodes in the scene
    texture_nodes = [i for i in maya.cmds.ls(type='file') if is_valid_texture(i)]
    
    # initialize variables
    processed_textures = []
    error_textures = []
    skipped_textures = []
    
    # if no file texture nodes found in scene, print warning, and return
    if not texture_nodes:
        maya.cmds.warning('No textures found, exiting')
        return (processed_textures, error_textures, skipped_textures)
    
    # iterate through file texture nodes
    for name in texture_nodes:
        # print file texture name
        print 'Processing texture', name
        as_type = None
        status = False
        texture = None
        
        # check the end suffix, set appropriate flag
        if '_diff' in name:
            status, texture = process_diffuse(name, out_dir)
            if status:
                processed_textures.append(texture)
                as_type = 'diffuse'
            else:
                error_textures.append(texture)
        elif '_spec' in name:
            status, texture = process_diffuse(name, out_dir)
            if status:
                processed_textures.append(texture)
                as_type = 'specular'
            else:
                error_textures.append(texture)
        elif '_bump' in name:
            status, texture = process_diffuse(name, out_dir)
            if status:
                processed_textures.append(texture)
                as_type = 'bump'
            else:
                error_textures.append(texture)
                
        # if status return, proceed accordingly and print the file texture name and its type
        if status:
            print 'Processed %s as a %s texture' % (texture, as_type)
        else:
            print 'Failed to process %s' % name
    try:
        # Rename the scene file with its directory path
        maya.cmds.file(rename=os.path.join(out_dir, new_file))
        # Try saving the file
        maya.cmds.file(save=True)
    except:
        # On error saving, print message
        print 'Error saving file, %s not saved.' % new_file
    finally:
        return (processed_textures, error_textures, skipped_textures)

def is_valid_texture(file_node):
    """
    Return whether or not the specified file node is actually connected to any models
    
    file_node = name of the file texture node (string or unicode)
    """
    # Returns a list of shaders having incoming connection from outColor of the file node
    shaders = maya.cmds.listConnections('%s.outColor' % file_node, destination=True)
    if not shaders:
        return False
    for shader in shaders:
        # Returns a list of shading groups having incoming connection from outColor of the shader node
        groups = maya.cmds.listConnections('%s.outColor' % shader)
        if not groups:
            return False
        for group in groups:
            # Returns a list of shape nodes (nodeType=mesh) connected to a SG
            meshes = maya.cmds.listConnections(group, type='mesh')
            if meshes:
                # Then it checks if the file node texture is either diffuse, bump or specular.
                if '_diff' in file_node:
                    return True
                elif '_spec' in file_node:
                    return True
                elif '_bump' in file_node:
                    return True
    return False

def process_diffuse(file_node, out_dir):
    """
    Process a file node's texture, reassign the new texture and return a status
    and texture name.
    
    file_node = Name of the texture file node (string or unicode)
    out_dir = Home directory (string)
    """
    status = False
    texture = None
    # get the name of the image file in the file texture node (fileTextureName (ftn))
    file_name = maya.cmds.getAttr('%s.ftn' % file_node)
    meshes = []
    # get the list of all shaders connected from the file texture node
    shaders = maya.cmds.listConnections('%s.outColor'% file_node, destination=True)
    if shaders:
        for s in shaders:
            # get a list of shading groups connected from the shader
            groups = maya.cmds.listConnections('%s.outColor'%s)
            if groups:
                for g in groups:
                    # get a list of shape nodes connected from the shading group
                    m = maya.cmds.listConnections(g, type='mesh')
                    if m:
                        meshes += m
    try:
        # processing code would be here
        new_file_name = file_name
        
        # Create a new blinn shader and assign a name
        shader = maya.cmds.shadingNode('blinn', asShader=True)
        
        # Create a set renderable set, an empty shading group
        shading_group = maya.cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        
        # Connect the shader to the shading group
        maya.cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')
        
        # create a place2dTexture node along with a file texture node. It like clicking the file node
        # in hypershade to create a new one. It automatically creates and connects a place2dTexture node.
        texture = maya.mel.eval('createRenderNodeCB -as2DTexture ""file""')
        
        # Put the name of the image file in the texture file node
        maya.cmds.setAttr(texture + '.ftn', new_file_name, type='string')
        
        # Connect the file texture node to the shader
        maya.cmds.connectAttr(texture + '.outColor', shader + '.color')
        
        # Assign the shading group to the meshes
        for mesh in meshes:
            maya.cmds.sets(mesh, edit=True, forceElement=shading_group)
        status=True
    except:
        texture = file_node
        status = False
    return (status, texture)
        
    
