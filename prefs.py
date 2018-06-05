import bpy


@property
def isDebug():
    # return True
    return bpy.app.debug_value != 0


class PixelGridPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    pixel_grid_color = bpy.props.FloatVectorProperty(name="pixel_grid_color",
                                                     subtype="COLOR",
                                                     default=(0.1, 0.1, 0.1, 0.2),
                                                     min=0.0, max=1.0,
                                                     size=4)

    def draw(self, context):
        layout = self.layout

        row = layout.row()

        row.prop(self, "pixel_grid_color", text="Pixel Grid Color")
