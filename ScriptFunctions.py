# Give Python access to Blender functionality 
import bpy

# random lib
import random

def scene_purge():
    # Select all objs
    bpy.ops.object.select_all(action='SELECT')

    # delete all selected objs
    bpy.ops.object.delete()

    # delete selected objs
    bpy.ops.outliner.orphans_purge()
    
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

    # set roughnes value
    principled_bsdf_node.inputs["Roughness"].default_value = random.random()
    
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