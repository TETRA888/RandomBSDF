# Give Python access to Blender functionality 
import bpy

# random lib
import random

import math

def scene_purge():
    # Select all objs
    bpy.ops.object.select_all(action='SELECT')

    # delete all selected objs
    bpy.ops.object.delete()

    # delete selected objs
    bpy.ops.outliner.orphans_purge()
    
def create_noise_mask(material):
    """Create multiple shader nodes and then connect them via code"""
    node_location_x_step = 300
    current_node_location_x = -node_location_x_step
    
    # create color ramp node
    color_ramp_node = material.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].position = random.random()
    color_ramp_node.color_ramp.elements[1].position = random.random()
    color_ramp_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    
    # create a Noise Texture node
    noise_texture_node = material.node_tree.nodes.new(type = "ShaderNodeTexNoise")
    noise_texture_node.inputs[2].default_value = random.uniform(0,20)
    noise_texture_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    
    # create a Mapping node
    mapping_node = material.node_tree.nodes.new(type = "ShaderNodeMapping")
    mapping_node.inputs[2].default_value[0] = random.uniform(0,math.radians(360))
    mapping_node.inputs[2].default_value[1] = random.uniform(0,math.radians(360))
    mapping_node.inputs[2].default_value[2] = random.uniform(0,math.radians(360))
    mapping_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step 

    # create a texture coordinate node
    texture_coordinate_node = material.node_tree.nodes.new(type = "ShaderNodeTexCoord")
    texture_coordinate_node.location.x = current_node_location_x
    
    material.node_tree.links.new(noise_texture_node.outputs["Color"],
                                color_ramp_node.inputs["Fac"])
                                
    material.node_tree.links.new(mapping_node.outputs["Vector"],
                                noise_texture_node.inputs["Vector"])
                                
    material.node_tree.links.new(texture_coordinate_node.outputs["Generated"],
                                mapping_node.inputs["Vector"])
    return color_ramp_node

def create_color(name):
    # create new material
    material = bpy.data.materials.new(name = name)

    # enable creating a material via nodes
    material.use_nodes = True

    # get ref to the principled bsdf shader node
    principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]
     
    # create base color of the material
    principled_bsdf_node.inputs["Base Color"].default_value = (random.random(), random.random(), random.random(), 1) # "Base Color " == index 0

    # set metallic value
    principled_bsdf_node.inputs["Metallic"].default_value = random.randint(0,1)

    # set roughness value
    principled_bsdf_node.inputs["Roughness"].default_value = random.random()
    
    color_ramp_node = create_noise_mask(material)

    #Connect the nodes
    material.node_tree.links.new(color_ramp_node.outputs["Color"], 
                            principled_bsdf_node.inputs["Roughness"])
    
    return material

def create_mesh():
    # create ico sphere
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 5)
    bpy.ops.object.shade_smooth()

    current_obj = bpy.context.active_object
    
    return current_obj

def main():
    scene_purge()
    name = "Oh material!"
    material = create_color(name)
    
    current_obj = create_mesh()
    
    # apply material to mesh object
    current_obj.data.materials.append(material)

main()