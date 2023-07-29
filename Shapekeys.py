import bpy

def get_shapekey(object_name, shape_name):
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    if bpy.context.object.data.shape_keys == None:
        return None
    for shape_key in bpy.context.object.data.shape_keys.key_blocks:
        if shape_key.name == shape_name:
            return shape_key

def reset_pose(root_object):
    bpy.context.view_layer.objects.active = root_object
    bpy.ops.object.posemode_toggle()
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()
    bpy.ops.object.posemode_toggle()

root = bpy.context.active_object
face_obj = bpy.data.objects["Face"]

if "Avatar" not in root.name and "Player" not in root.name:
    raise BaseException("Avatar/Player object is not selected.")

if face_obj is None:
    raise BaseException("Not found the Face object.")

bpy.ops.object.mode_set(mode='OBJECT')
reset_pose(root)

# add basis shape
if get_shapekey("Face", "Basis") == None:
    bpy.context.view_layer.objects.active = bpy.data.objects["Face"]
    bpy.ops.object.shape_key_add(from_mix=False)

# convert animation to shapekey
for action in bpy.data.actions:
    if ".00" in action.name or "Emo_" not in action.name:
        continue

    print(action.name)    
    arr = action.name.split("_")
    shapekey_name = "_".join(arr[2:])

    # apply animation
    root.animation_data.action = action
    bpy.ops.object.visual_transform_apply()
    
    # convert shapekay
    bpy.context.view_layer.objects.active = face_obj
    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=root.name)
    shapekey = get_shapekey(face_obj.name, root.name)
    shapekey.name = shapekey_name

    # reset transform
    reset_pose(root)

# remove all actions
# for action in bpy.data.actions:
#     bpy.data.actions.remove(action)
