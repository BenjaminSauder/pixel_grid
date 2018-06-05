bl_info = {
    "name": "Pixel Grid",
    "category": "3D View",
    "author": "Benjamin Sauder",
    "description": "Show pixel grid in 3d view",
    "version": (0, 1),
    "location": "Camera Properties > Display",
    "blender": (2, 79, 0),
}

if "bpy" in locals():
    import importlib

    importlib.reload(main)
    importlib.reload(render)
    importlib.reload(ui)
    importlib.reload(prefs)
    importlib.reload(op_snap_verts_to_render_pixel)

else:
    from . import (
        main,
        render,
        ui,
        prefs,
        op_snap_verts_to_render_pixel,

    )

import bpy
from bpy.app.handlers import persistent

# stuff which needs to be registred in blender
classes = [
    prefs.PixelGridPrefs,
    op_snap_verts_to_render_pixel.SnapVertsToRenderPixel,
]


@persistent
def scene_update_post_handler(dummy):
    main.update()


def register():
    if prefs.isDebug:
        print("register")

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.pixel_grid_visible = bpy.props.BoolProperty(
        name="pixel_grid_visible",
        default=False)

    bpy.types.DATA_PT_camera_display.prepend(ui.camera_display_extension)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(ui.vertices_menu_extension)

    bpy.app.handlers.scene_update_post.append(scene_update_post_handler)


def unregister():
    if prefs.isDebug:
        print("unregister")

    for k, v in main.VIEW3D.items():
        bpy.types.SpaceView3D.draw_handler_remove(v, 'WINDOW')

    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(ui.vertices_menu_extension)

    for c in classes:
        bpy.utils.unregister_class(c)


    del bpy.types.Scene.pixel_grid_visible
