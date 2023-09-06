import bpy


icones = None


class MC_tool_MapOptimiz_prop(bpy.types.PropertyGroup):
    is_weld: bpy.props.BoolProperty(
        name="是否焊接", description="焊接网格过于接近的点 可针对楼梯 水这类的方块", default=False
    )
    bool_ismap: bpy.props.BoolProperty(name="是否拼接", default=False)


class MC_Tool_ModelFXBake_prop(bpy.types.PropertyGroup):
    frame_start: bpy.props.IntProperty(name="帧开始", description="烘焙开始", default=0)
    frame_end: bpy.props.IntProperty(name="帧结束", description="烘焙结束", default=250)
    bake_x_resolution: bpy.props.IntProperty(name="x_分辨率", default=256)
    bake_y_resolution: bpy.props.IntProperty(name="y_分辨率", default=256)
