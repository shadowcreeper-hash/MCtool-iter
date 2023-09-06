import bpy
import os
from bpy.utils import previews
from .ops import MC_Tool_MapOptimiz_Ops
from .ops import MC_Tool_ModelFXBake_Ops
from .ui import ShadowCreeper_MC_Tool_MapOptimiz_Panel
from .ui import ShadowCreeper_MC_Tool_ModelFXBake_Panel
from .props import MC_tool_MapOptimiz_prop
from .props import MC_Tool_ModelFXBake_prop
from .props import icones


bl_info = {
    "name": "Minecraft cg tool:iter",
    "description": "this is the tool can help your minecraft animation make",
    "author": "iter 埃特 (shadow creeper)",
    "version": (0, 0, 8),
    "blender": (3, 1, 0),
    "location": "View3D",
    "warning": "This addon is still in development.插件还在开发中.",
    "wiki_url": "https://space.bilibili.com/472637101",
    "category": "Object"}


def register():
    bpy.utils.register_class(ShadowCreeper_MC_Tool_MapOptimiz_Panel)
    bpy.utils.register_class(ShadowCreeper_MC_Tool_ModelFXBake_Panel)
    bpy.utils.register_class(MC_Tool_MapOptimiz_Ops)
    bpy.utils.register_class(MC_Tool_ModelFXBake_Ops)
    bpy.utils.register_class(MC_tool_MapOptimiz_prop)
    bpy.utils.register_class(MC_Tool_ModelFXBake_prop)

    bpy.types.Scene.mc_tool_mapOptimiz_prop = bpy.props.PointerProperty(
        type=MC_tool_MapOptimiz_prop)
    bpy.types.Scene.mc_tool_modelbake_prop = bpy.props.PointerProperty(
        type=MC_Tool_ModelFXBake_prop)
    props.icones = bpy.utils.previews.new()
    props.icones.load('logo', os.path.join(
        os.path.dirname(__file__), 'icons', 'logo.png'), 'IMAGE')


def unregister():
    bpy.utils.unregister_class(ShadowCreeper_MC_Tool_MapOptimiz_Panel)
    bpy.utils.unregister_class(ShadowCreeper_MC_Tool_ModelFXBake_Panel)
    bpy.utils.unregister_class(MC_Tool_MapOptimiz_Ops)
    bpy.utils.unregister_class(MC_Tool_ModelFXBake_Ops)
    bpy.utils.unregister_class(MC_tool_MapOptimiz_prop)
    bpy.utils.unregister_class(MC_Tool_ModelFXBake_prop)
    bpy.utils.previews.remove(props.icones)
    del bpy.types.Scene.mc_tool_mapOptimiz_prop
    del bpy.types.Scene.mc_tool_modelbake_prop


if __name__ == "__main__":
    register()
