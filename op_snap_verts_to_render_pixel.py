import bpy

from . import main


class SnapVertsToRenderPixel(bpy.types.Operator):
    """ 
    Snaps vertices to the closest render pixel.
    Needs an orthographic camera to work.
    """
    bl_idname = "mesh.snap_verts_to_render_pixel"
    bl_label = "Snap Vertices to Render Pixels"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            #print("invalid object selection")
            return {'CANCELLED'}

        mesh = obj.data
        scene = context.scene
        camera = scene.camera

        if not camera or camera.data.type != "ORTHO":
            self.report({'ERROR_INVALID_INPUT'}, "The scene camera must be in orthographic mode or the scene camera is missing.")
            return {'CANCELLED'}

        currentMode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        ortho_scale = camera.data.ortho_scale

        resolution_percentage = scene.render.resolution_percentage / 100.0

        renderpixel_size = (ortho_scale / (scene.render.resolution_x * resolution_percentage),
                            ortho_scale / (scene.render.resolution_y * resolution_percentage))

        # print(renderpixel_size)
        for vert in mesh.vertices:
            if not vert.select:
                continue

            co = obj.matrix_world * vert.co
            co_ortho = camera.matrix_world.inverted() * co

            co_ortho.x = roundToValue(co_ortho.x, base=renderpixel_size[0])
            co_ortho.y = roundToValue(co_ortho.y, base=renderpixel_size[1])

            co_world = camera.matrix_world * co_ortho

            vert.co = obj.matrix_world.inverted() * co_world


        bpy.ops.object.mode_set(mode=currentMode)
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


def roundToValue(x, prec=16, base=.05):
    return round(base * round(float(x) / base), prec)
