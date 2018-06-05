# Pixel Grid
A small utility addon to display render pixels in the scene camera view.
It comes with an operator to snap vertices to the render pixels of an orthographic camera.

The addon does take "Render Resolution" and "Percentage Scale" into consideration. Camera Shift should also work as well.

After installation a small "pixel grid" checkbox should appear in the camera properties > display tab.

![pixel_grid_header](https://github.com/BenjaminSauder/pixel_grid/blob/master/doc/header.jpg)


## Snap Verts to Render Pixel

This little operator is found under Mesh>Vertices>Snap Vertices to Render Pixels. It can also be called via spacebar-search: "Snap Vertices to Render Pixels"

For this thing to work you have to select a mesh object, and the scene camera has to be set to orthographic mode.

![pixel_grid_snap_verts](https://github.com/BenjaminSauder/pixel_grid/blob/master/doc/snap_verts.gif)

# Installation

- download .zip from the repo: https://github.com/BenjaminSauder/pixel_grid/archive/master.zip
- rename the zip to "pixel_grid" - this is important!
- install via user preferences > install addon from file...
- addon should be listed under Camera > Pixel Grid
