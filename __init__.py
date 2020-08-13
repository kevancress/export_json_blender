# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "json_export",
    "author" : "Kevan Cress",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location": "File > Import-Export",
    "warning" : "",
    "category": "Import-Export",
    
}

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
)
from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
    orientation_helper,
    axis_conversion,
)
from bpy.types import (
    Operator,
    OperatorFileListElement,
)


class ExportJSON(Operator, ImportHelper):
    bl_idname = "export_mesh.json"
    bl_label = "Export"
    bl_description = "Export Mesh Verticies as JSON data"
    bl_options = {'UNDO'}

    filename_ext = ".json"

    use_selection: BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=False,
    )

    def execute(self, context):

        scene = context.scene
        if self.use_selection:
            objs = context.selected_objects
        else:
            objs = scene.objects

        jsonStr = "{"
        for obj in objs:
            mesh = obj.data
            verts = mesh.vertices
            jsonStr += "\n \"" + obj.name + '\":'
            
            jsonStr += '['
            for vert in verts:

                jsonStr += "\n \t {"
                coord = vert.co
                jsonStr += "\"x\":" + str(coord[0]) + ', '
                jsonStr += "\"y\":" + str(coord[1])  + ', '
                jsonStr += "\"z\":" + str(coord[2])

                jsonStr += '},'

            jsonStr = jsonStr[:-1]
            jsonStr += '],'

        jsonStr = jsonStr[:-1]
        jsonStr += "\n }"
        print("exporting JSON")
        print(jsonStr)

        with open(self.filepath, "w") as f:
            f.write(jsonStr)



        return{'FINISHED'}

        

    
    def draw(self, context):
        pass


class JSON_PT_export_main(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = ""
    bl_parent_id = "FILE_PT_operator"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_MESH_OT_json"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, "use_selection")

classes = (
    ExportJSON,
    JSON_PT_export_main,
)

def menu_export(self, context):
    self.layout.operator(ExportJSON.bl_idname, text="JSON (.json)")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(menu_export)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_export.remove(menu_export)

if __name__ == "__main__":
    register()