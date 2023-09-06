import bpy
from .utils import MC_Tool_Fun
from . import props


class MC_Tool_MapOptimiz_Ops(bpy.types.Operator):
    bl_idname = "ethevat.mapoptimiz"
    bl_label = "地图优化"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    def execute(self, context):
        MC_Tool_Fun.MapOptimize(
            context, context.scene.mc_tool_mapOptimiz_prop.is_weld)
        return {"FINISHED"}


class MC_Tool_ModelFXBake_Ops(bpy.types.Operator):
    bl_idname = "scc.modelfxbake_ops"
    bl_label = "烘焙生成数据"
    bl_description = "烘焙生成数据"
    bl_options = {"REGISTER"}

    def execute(self, context):
        mc_tool_modelbake_prop = bpy.context.scene.mc_tool_modelbake_prop
        MC_Tool_Fun.ModelBake(context,
                              startframe=mc_tool_modelbake_prop.frame_start,
                              endframe=mc_tool_modelbake_prop.frame_end,
                              x_resolution=mc_tool_modelbake_prop.bake_x_resolution,
                              y_resolution=mc_tool_modelbake_prop.bake_y_resolution)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {"FINISHED"}
