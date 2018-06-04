import math

import bpy
import bgl
from bpy_extras.view3d_utils import location_3d_to_region_2d

from . import main

GRID_MIN_SIZE = 4

COLOR_RED = (1.0, 0.0, 0.0, 1.0)
COLOR_GRID = (0.1, 0.1, 0.1, 0.2)


def draw_callback_view3D(area, v3d, rv3d):
    if (area not in main.VIEW3D or len(area.regions) == 0 or
        bpy.context.scene.camera == None or
        area.type != "VIEW_3D" or rv3d.view_perspective != 'CAMERA' or
        not bpy.context.scene.pixel_grid_visible ):
        return


    scene = bpy.context.scene

    viewport_info = bgl.Buffer(bgl.GL_INT, 4)
    bgl.glGetIntegerv(bgl.GL_VIEWPORT, viewport_info)

    region = None
    for r in area.regions:
        if r.type == "WINDOW":
            region = r
            width = region.width
            height = region.height
            region_x = region.x
            region_y = region.y


    bgl.glViewport(region_x, region_y, width, height)

    camera_frame = view3d_camera_border(region, rv3d)
    # print(camera_frame)

    resolution_percentage = scene.render.resolution_percentage / 100.0

    resolution_x = int(scene.render.resolution_x * resolution_percentage)
    resolution_y = int(scene.render.resolution_y * resolution_percentage)



    # TopRight - BottomLeft
    screen_resolution = camera_frame[0] - camera_frame[2]

    screen_x = screen_resolution.x / resolution_x
    screen_y = screen_resolution.y / resolution_y

    #calculate the offset with shift, and take care of modulus returning only positive
    shift_x = (screen_x * (scene.camera.data.shift_x % 1.0))
    if scene.camera.data.shift_x < 0:
        shift_x = -shift_x
    shift_y = (screen_y * (scene.camera.data.shift_y % 1.0))
    if scene.camera.data.shift_y < 0:
        shift_y = -shift_y

    # generate grid
    vertices = []
    alpha = 0

    if screen_x > GRID_MIN_SIZE and screen_y > GRID_MIN_SIZE:
        for x in range(resolution_x):
            position_x = camera_frame[3].x + x * screen_x + shift_x
            vertices.extend((position_x,
                             camera_frame[0].y,
                             position_x,
                             camera_frame[2].y))

        for y in range(resolution_y):
            position_y = camera_frame[0].y - y * screen_y + shift_y
            vertices.extend((camera_frame[2].x,
                             position_y,
                             camera_frame[0].x,
                             position_y))


        #fade in pixel grid
        alpha = maprange((GRID_MIN_SIZE, GRID_MIN_SIZE * 4), (0, 1.0), min(screen_x, screen_y))
        alpha = min(1.0 , max(0, alpha))

        '''
        vertices = [0, 0,
                    100, 0,
    
                    0, 0,
                    100, 100,
    
                    0, 0,
                    0, 100,
    
                    0, 0,
                    100, 100,
                 ]
        '''

    create_vao("grid", vertices)

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

    color = (COLOR_GRID[0], COLOR_GRID[1], COLOR_GRID[2], COLOR_GRID[3] * alpha)
    print(color)
    draw_vertex_array("grid", bgl.GL_LINES, 2, color)

    bgl.glViewport(*tuple(viewport_info))


# https://blender.stackexchange.com/questions/6377/coordinates-of-corners-of-camera-view-border
def view3d_camera_border(region, rv3d):
    scene = bpy.context.scene
    obj = scene.camera
    cam = obj.data

    frame = cam.view_frame(scene)

    # move from object-space into world-space
    frame = [obj.matrix_world * v for v in frame]

    # move into pixelspace
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]

    # returns RightTop RightBottom LeftBottom LeftTop
    return frame_px


def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


# Open GL Shader Part
VAO = {}


def create_vao(name, verts):
    vao = None

    if len(verts) > 0:
        vao = bgl.Buffer(bgl.GL_FLOAT, len(verts), verts)

    VAO[name] = vao


shaderVertString = """
void main()
{
    gl_Position =  ftransform();
}
"""

shaderFragString = """
uniform vec4 color;
void main()
{
    gl_FragColor = color;
}
"""

program = None


def compile_shader():
    global program
    program = bgl.glCreateProgram()

    shaderVert = bgl.glCreateShader(bgl.GL_VERTEX_SHADER)
    shaderFrag = bgl.glCreateShader(bgl.GL_FRAGMENT_SHADER)

    bgl.glShaderSource(shaderVert, shaderVertString)
    bgl.glShaderSource(shaderFrag, shaderFragString)

    bgl.glCompileShader(shaderVert)
    bgl.glCompileShader(shaderFrag)

    bgl.glAttachShader(program, shaderVert)
    bgl.glAttachShader(program, shaderFrag)

    bgl.glLinkProgram(program)

    bgl.glDeleteShader(shaderVert)
    bgl.glDeleteShader(shaderFrag)


def draw_vertex_array(key, mode, dimensions, color):
    if key in VAO and VAO[key] and program:
        vao = VAO[key]

        bgl.glUseProgram(program)
        bgl.glUniform4f(bgl.glGetUniformLocation(program, "color"), *color)

        bgl.glEnableClientState(bgl.GL_VERTEX_ARRAY)
        bgl.glVertexPointer(dimensions, bgl.GL_FLOAT, 0, vao)
        bgl.glDrawArrays(mode, 0, int(len(vao) / dimensions))

        bgl.glDisableClientState(bgl.GL_VERTEX_ARRAY)
        bgl.glUseProgram(0)


compile_shader()
