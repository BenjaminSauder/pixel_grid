bl_info = {
    "name": "Pixel Grid",
    "category": "3D View",
    "author": "Benjamin Sauder",
    "description": "Show pixel grid in 3d view",
    "version": (0, 1),
    "location": "View3D  > Tool Shelf",
    "blender": (2, 79, 0),
}

if "bpy" in locals():
    import importlib

    importlib.reload(main)
    importlib.reload(render)
    importlib.reload(ui)
    importlib.reload(op_snap_verts_to_render_pixel)

else:
    from . import (
        main,
        render,
        ui,
        op_snap_verts_to_render_pixel,

    )

import bpy
from bpy.app.handlers import persistent

# stuff which needs to be registred in blender
classes = [
    op_snap_verts_to_render_pixel.SnapVertsToRenderPixel,
]


@property
def isDebug():
    #return True
    return  bpy.app.debug_value != 0


@persistent
def scene_update_post_handler(dummy):
    main.update()


def register():
    if isDebug:
        print("register")

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.pixel_grid_visible = bpy.props.BoolProperty(
        name="pixel_grid_visible",
        default=False)

    bpy.types.DATA_PT_camera_display.prepend(ui.camera_display_extension)


    bpy.app.handlers.scene_update_post.append(scene_update_post_handler)


def unregister():
    if isDebug:
        print("unregister")

    for k,v in main.VIEW3D.items():
        bpy.types.SpaceView3D.draw_handler_remove(v, 'WINDOW')

    for c in classes:
        bpy.utils.unregister_class(c)
