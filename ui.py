import bpy
from . import props
from .ops import MC_Tool_MapOptimiz_Ops
from .ops import MC_Tool_ModelFXBake_Ops


class ShadowCreeper_MC_Tool_MapOptimiz_Panel(bpy.types.Panel):
    bl_idname = "ShadowCreeper_Tool_PL"
    bl_label = "MC工具箱-iter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MC动画工具箱-iter"

    def draw(self, context):
        layout = self.layout
        layout.row()
        layout.operator(
            MC_Tool_MapOptimiz_Ops.bl_idname, icon_value=props.icones["logo"].icon_id
        )

        layout.prop(context.scene.mc_tool_mapOptimiz_prop, "is_weld")
        layout.prop(context.scene.mc_tool_mapOptimiz_prop, "bool_ismap")


class ShadowCreeper_MC_Tool_ModelFXBake_Panel(bpy.types.Panel):
    bl_idname = "scc-modelfxbake_pl"
    bl_label = "烘焙序列_精灵贴图"
    bl_description = "Description that shows in blender tooltips"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = ""

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.mc_tool_modelbake_prop, "frame_start")
        layout.prop(context.scene.mc_tool_modelbake_prop, "frame_end")
        layout.prop(context.scene.mc_tool_modelbake_prop, "bake_x_resolution")
        layout.prop(context.scene.mc_tool_modelbake_prop, "bake_y_resolution")
        layout.operator(MC_Tool_ModelFXBake_Ops.bl_idname)
