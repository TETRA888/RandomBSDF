# Give Python access to Blender functionality 
import bpy

# random lib
import random

# Select all objs
bpy.ops.object.select_all(action='SELECT')

# delete all selected objs
bpy.ops.object.delete()

# delete selected objs
bpy.ops.outliner.orphans_purge()

# create new material
material = bpy.data.materials.new(name = "Generated_Material")

# enable creating a material via nodes
material.use_nodes = True

# get ref to the principled bsdf shader node
principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]
 
# create base color of the material
principled_bsdf_node.inputs["Base Color"].default_value = (0.800086, 0.0185655, 0.0156113, 1) # "Base Color " == index 0

# set metallic value
principled_bsdf_node.inputs["Metallic"].default_value = 1.0

# set roughnes value
principled_bsdf_node.inputs["Roughness"].default_value = 0.5

# create ico sphere
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 5)
bpy.ops.object.shade_smooth()

current_obj = bpy.context.active_object

# apply material to mesh object
current_obj.data.materials.append(material)
