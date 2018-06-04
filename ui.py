import bpy

def camera_display_extension(self, context):
    layout = self.layout
    row = layout.row()
    row.prop(bpy.context.scene, "pixel_grid_visible", text="Pixel Grid")

