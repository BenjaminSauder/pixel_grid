import bpy
import time

from . import render

last_update = 0
UPDATE_RATE = 0.1

VIEW3D = {}


def update():
    global last_update

    # we can live with a lower update rate here..
    if time.time() < last_update:
        return

    last_update = time.time() + UPDATE_RATE

    global VIEW3D

    # find all view3d and add drawhandler if necessary
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == "WINDOW":

                    v3d = area.spaces[0]
                    rv3d = v3d.region_3d

                    if area not in VIEW3D:
                        #print("adding view3d:", v3d)
                        args = area, v3d, rv3d
                        handle = v3d.draw_handler_add(render.draw_callback_view3D, args, 'WINDOW', 'POST_PIXEL')
                        VIEW3D[area] = handle

    # remove all closed view3d draw handlers
    closed_views = filter(lambda v3d: len(v3d.regions) == 0, list(VIEW3D.keys()))
    for closed_view in closed_views:
        #print("remove view3d")
        bpy.types.SpaceView3D.draw_handler_remove( VIEW3D[closed_view], 'WINDOW')
        VIEW3D.pop(closed_view, None)


def get_camera_shift(scene, stepsize_x, stepsize_y):
    # calculate the offset with shift, and take care of modulus returning only positive
    shift_x = (stepsize_x * (scene.camera.data.shift_x % 1.0))
    if scene.camera.data.shift_x < 0:
        shift_x = -shift_x
    shift_y = (stepsize_y * (scene.camera.data.shift_y % 1.0))
    if scene.camera.data.shift_y < 0:
        shift_y = -shift_y

    return shift_x, shift_y