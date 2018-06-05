import bpy

from . import  op_snap_verts_to_render_pixel

def camera_display_extension(self, context):
    layout = self.layout
    row = layout.row()
    row.prop(bpy.context.scene, "pixel_grid_visible", text="Pixel Grid")


def vertices_menu_extension(self, context):
    self.layout.operator(op_snap_verts_to_render_pixel.SnapVertsToRenderPixel.bl_idname, text='Snap Vertices to Render Pixels')