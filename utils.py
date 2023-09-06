import bpy
import os

from .props import MC_tool_MapOptimiz_prop


class MC_Tool_Fun:
    def check_words(string, target_words):
        for word in target_words:
            if word in string:
                return True
        return False

    def AppleNode(context, nodename: str):
        bpy.ops.object.modifier_add(type="NODES")
        mg = context.active_object.modifiers[0]
        try:
            mg.node_group = bpy.data.node_groups[nodename]
        except:
            path = __file__.rsplit("\\", 1)[0] + "\\blend_libraries\\map_node.blend"
            with bpy.data.libraries.load(path) as (data_from, data_to):
                strs = nodename
                if strs in nodename:
                    if not strs in bpy.data.node_groups:
                        data_to.node_groups = [strs]
        mg.node_group = bpy.data.node_groups[nodename]
        bpy.ops.object.modifier_apply(modifier=mg.name)

    def MapOptimize(context, is_weld: bool):
        mc_tool_mapOptimiz_prop: MC_tool_MapOptimiz_prop = (
            context.scene.mc_tool_mapOptimiz_prop
        )
        objs = context.selected_objects
        worlduv_node = "世界空间映射uv"
        centeruv_node = "centeruv"
        Slab_kill_node = "Slab_kill"
        Plan_kill_node = "Plan_kill"
        for obj in objs:
            # 遍历选中
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="OBJECT")
            # 移除多余的修改器
            for md in context.active_object.modifiers:
                context.active_object.modifiers.remove(md)
            # 检测避免方块
            if MC_Tool_Fun.check_words(
                obj.name,
                [
                    "Gate",
                    "Wall",
                    "Rod",
                    "Rail",
                    "Lantern",
                    "Cobweb",
                    "Grindstone",
                    "Sensor",
                    "Trapdoor",
                    "Bars",
                    "Anvil",
                    "Stairs",
                    "Fence",
                    "Chain",
                    "Lectern",
                    "Leaves",
                    "Sapling",
                    "Grass.",
                    "Slab",
                ],
            ):
                continue
            # 合并玻璃和水
            if MC_Tool_Fun.check_words(
                obj.name, ["Water", "Glass_Pane", "Fence", "Wall", "Door"]
            ):
                modify_obj = obj.modifiers.new("Weld", "WELD")
                bpy.ops.object.modifier_apply(modifier=modify_obj.name)
            if MC_Tool_Fun.check_words(
                obj.name, ["Glass_Pane", "Fence", "Wall", "Door"]
            ):
                MC_Tool_Fun.AppleNode(context, Plan_kill_node)
            # 如果包含半砖台阶 针对性删面
            if "Slab" in obj.name:
                break
                bpy.ops.object.modifier_add(type="NODES")
                mg = context.active_object.modifiers[0]
                try:
                    mg.node_group = bpy.data.node_groups[Slab_kill_node]
                except:
                    path = (
                        __file__.rsplit("\\", 1)[0]
                        + "\\blend_libraries\\map_node.blend"
                    )
                    with bpy.data.libraries.load(path) as (data_from, data_to):
                        strs = Slab_kill_node
                        if strs in Slab_kill_node:
                            if not strs in bpy.data.node_groups:
                                data_to.node_groups = [strs]
                mg.node_group = bpy.data.node_groups[Slab_kill_node]
                bpy.ops.object.modifier_apply(modifier=mg.name)
            # 添加uv存储
            bpy.ops.object.modifier_add(type="NODES")
            mg = obj.modifiers[0]
            try:
                mg.node_group = bpy.data.node_groups[centeruv_node]
            except:
                path = __file__.rsplit("\\", 1)[0] + "\\blend_libraries\\map_node.blend"
                with bpy.data.libraries.load(path) as (data_from, data_to):
                    strs = centeruv_node
                    if strs in centeruv_node:
                        if not strs in bpy.data.node_groups:
                            data_to.node_groups = [strs]
            mg.node_group = bpy.data.node_groups[centeruv_node]

            bpy.ops.object.modifier_apply(modifier=mg.name)

            # 添加精简修改器并且应用
            modify_obj = obj.modifiers.new("Decimate", "DECIMATE")
            modify_obj.decimate_type = "DISSOLVE"
            modify_obj.delimit = {"MATERIAL"}
            bpy.ops.object.modifier_apply(modifier=modify_obj.name)
            bpy.ops.object.modifier_add(type="NODES")
            mg = obj.modifiers[0]
            context.active_object.modifiers.active = mg
            try:
                mg.node_group = bpy.data.node_groups[worlduv_node]
            except:
                path = __file__.rsplit("\\", 1)[0] + "\\blend_libraries\\map_node.blend"
                with bpy.data.libraries.load(path) as (data_from, data_to):
                    strs = worlduv_node
                    if strs in worlduv_node:
                        if not strs in bpy.data.node_groups:
                            data_to.node_groups = [strs]
            mg.node_group = bpy.data.node_groups[worlduv_node]
            obj.modifiers[0]["Output_2_attribute_name"] = obj.data.uv_layers.active.name
            bpy.ops.object.modifier_apply(modifier=mg.name)
            atts = obj.data.attributes
            max = len(atts)
            i = 0
            blender_version = bpy.app.version
            version_string = (
                f"{blender_version[0]}.{blender_version[1]}{blender_version[2]:02}"
            )
            version_float = float(version_string)
            while i < max:
                if atts[i].data_type == "FLOAT_VECTOR" and atts[i].domain == "CORNER":
                    atts.active_index = i
                    print(blender_version)
                    if version_float < 3.4:
                        bpy.ops.geometry.attribute_convert(mode="UV_MAP")
                    else:
                        bpy.ops.geometry.attribute_convert(
                            mode="GENERIC", domain="CORNER", data_type="FLOAT2"
                        )

                    max -= 1
                    continue
                if atts[i].data_type == "FLOAT_COLOR" and atts[i].domain == "CORNER":
                    atts.active_index = i
                    bpy.ops.geometry.attribute_convert(
                        mode="GENERIC", domain="CORNER", data_type="BYTE_COLOR"
                    )
                    max -= 1
                    continue
                i += 1
            obj.select_set(False)
            if mc_tool_mapOptimiz_prop.bool_ismap:
                MC_Tool_Fun.addmat(objs)

    def addmat(objs):
        indexname = "world-uvmap-fix"
        try:
            node_group: bpy.types.ShaderNodeGroup = bpy.data.node_groups[indexname]
        except:
            path = __file__.rsplit("\\", 1)[0] + "\\blend_libraries\\map_node.blend"
            with bpy.data.libraries.load(path) as (data_from, data_to):
                strs = indexname
                if strs in indexname:
                    if not strs in bpy.data.node_groups:
                        data_to.node_groups = [strs]
        for obj in objs:
            # 检查物体是否有材质
            if obj.type == "MESH" and obj.data.materials:
                # 遍历物体的每个材质
                material: bpy.types.Material
                for material in obj.data.materials:
                    # 创建一个新的节点组
                    nodes = material.node_tree.nodes
                    shader_node: bpy.types.ShaderNodeGroup = nodes.new(
                        "ShaderNodeGroup"
                    )
                    node_group = bpy.data.node_groups.get(indexname)
                    # 在节点组中添加节点
                    shader_node.node_tree = node_group
                    for node in nodes:
                        # 检查节点是否是一个贴图节点
                        if node.type == "TEX_IMAGE":
                            teximage_node: bpy.types.ShaderNodeTexImage = node
                        # 连接节点
                        material.node_tree.links.new(
                            shader_node.outputs[0], teximage_node.inputs[0]
                        )

    def ModelBake(
        context, startframe: int, endframe: int, x_resolution: int, y_resolution: int
    ):
        bpy.data.scenes["Scene"].render.engine = "CYCLES"

        bpy.ops.object.mode_set(mode="OBJECT")
        obj = context.active_object
        mainname = obj.name
        imagess: list = []

        for i in range(startframe, endframe):
            context.scene.frame_set(i)
            fileindex = "%04d" % i
            filepath = os.path.dirname(bpy.data.filepath)
            filepath = filepath + "\\data"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            j: int = 0
            bpy.ops.object.duplicate_move()
            bpy.ops.object.apply_all_modifiers()

            ob = context.active_object
            atts = ob.data.attributes
            while j < len(atts):
                if atts[j].data_type == "FLOAT_VECTOR" and atts[j].domain == "CORNER":
                    atts.active_index = j
                    bpy.ops.geometry.attribute_convert(mode="UV_MAP")
                    j -= 1
                    print("uv yes")
                    continue
                if atts[j].data_type == "FLOAT_COLOR" and atts[j].domain == "CORNER":
                    atts.active_index = j
                    bpy.ops.geometry.attribute_convert(
                        mode="GENERIC", domain="CORNER", data_type="BYTE_COLOR"
                    )
                    j -= 1
                    print("col yes")
                    continue
                j += 1
            bpy.ops.export_scene.fbx(
                filepath=bpy.path.abspath(filepath + "\\" + mainname + "." + fileindex)
                + ".fbx",
                use_selection=True,
                global_scale=0.01,
                bake_anim=False,
            )
            images = MC_Tool_Fun.cycles_bake(
                context,
                name=mainname,
                filepath=filepath,
                x_resolution=x_resolution,
                y_resolution=y_resolution,
            )
            imagess.append(images)
            bpy.ops.object.delete(use_global=True)
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            context.scene.frame_set(i)
            context.scene.update_render_engine()
        i = 0
        max: int
        max = len(imagess[0])
        j: int
        for j in range(0, max):
            for images in imagess:
                bpy.ops.mesh.primitive_plane_add(size=1)
                bpy.context.active_object.location = (0, i, 0)
                bpy.ops.object.material_slot_add()
                mat = bpy.data.materials.new(name=images[j].name + str(i))
                mat.use_nodes = True

                bpy.context.active_object.material_slots[0].material = mat
                mat.blend_method = "BLEND"
                nodes = mat.node_tree.nodes
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                image_node = nodes.new("ShaderNodeTexImage")
                image_node.image = images[j]
                image_node.interpolation = "Closest"
                links = mat.node_tree.links
                links.new(image_node.outputs[0], bsdf.inputs[0])
                links.new(image_node.outputs[0], bsdf.inputs[19])
                links.new(image_node.outputs[1], bsdf.inputs[21])
                i += 1
            i = 0

    def cycles_bake(
        context, name, filepath, x_resolution: int, y_resolution: int
    ) -> list:
        obj = context.active_object
        frame = bpy.context.scene.frame_current
        frame = "%04d" % frame

        for mat_slot in obj.material_slots:
            if mat_slot.material == None:
                continue
            nameid = name + "_" + mat_slot.material.name + "." + str(frame)
            try:
                mat_slot.material.node_tree.nodes.active.image = bpy.data.images[nameid]
                bpy.ops.object.bake_image()
            except:
                bpy.ops.image.new(name=nameid, height=y_resolution, width=x_resolution)

            bpy.data.images[nameid].filepath = bpy.path.abspath(
                filepath + "\\" + nameid + ".png"
            )
            bpy.data.images[nameid].file_format = "PNG"
            bpy.data.images[nameid].save()
            mat_slot.material.node_tree.nodes.active.image = bpy.data.images[nameid]
            bpy.ops.object.bake_image()
        bpy.ops.object.bake()
        images_list: list = []
        for mat_slot in obj.material_slots:
            if mat_slot.material == None:
                continue
            nameid = name + "_" + mat_slot.material.name + "." + str(frame)
            bpy.data.images[nameid].save()
            images_list.append(bpy.data.images[nameid])
        return images_list
