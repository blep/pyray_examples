"""raylib [textures] example - Image loading and texture creation
Example complexity rating: [★★★★] 4/4
NOTE: Images are loaded in CPU memory (RAM); textures are loaded in GPU memory (VRAM)
Example contributed by Karim Salem (@kimo-s) and reviewed by Ramon Santamaria (@raysan5)
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Karim Salem (@kimo-s)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def normalize_kernel(kernel, size):
    """Normalize values in a kernel"""
    total = sum(kernel)
    
    if total != 0.0:
        for i in range(size):
            kernel[i] /= total
    
    return kernel

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - image convolution")

image = rl.load_image(str(THIS_DIR/"resources/cat.png"))  # Loaded in CPU memory (RAM)

# Define kernels for different effects
gaussian_kernel = [
    1.0, 2.0, 1.0,
    2.0, 4.0, 2.0,
    1.0, 2.0, 1.0
]

sobel_kernel = [
    1.0, 0.0, -1.0,
    2.0, 0.0, -2.0,
    1.0, 0.0, -1.0
]

sharpen_kernel = [
    0.0, -1.0, 0.0,
    -1.0, 5.0, -1.0,
    0.0, -1.0, 0.0
]

# Normalize kernels
gaussian_kernel = normalize_kernel(gaussian_kernel, 9)
sharpen_kernel = normalize_kernel(sharpen_kernel, 9)
sobel_kernel = normalize_kernel(sobel_kernel, 9)

# Apply kernels to create different image effects
cat_sharpened = rl.image_copy(image)
rl.image_kernel_convolution(cat_sharpened, sharpen_kernel, 9)

cat_sobel = rl.image_copy(image)
rl.image_kernel_convolution(cat_sobel, sobel_kernel, 9)

cat_gaussian = rl.image_copy(image)
for i in range(6):
    rl.image_kernel_convolution(cat_gaussian, gaussian_kernel, 9)

# Crop images to show side by side
rl.image_crop(image, rl.Rectangle(0, 0, 200, 450))
rl.image_crop(cat_gaussian, rl.Rectangle(0, 0, 200, 450))
rl.image_crop(cat_sobel, rl.Rectangle(0, 0, 200, 450))
rl.image_crop(cat_sharpened, rl.Rectangle(0, 0, 200, 450))

# Images converted to texture, GPU memory (VRAM)
texture = rl.load_texture_from_image(image)
cat_sharpened_texture = rl.load_texture_from_image(cat_sharpened)
cat_sobel_texture = rl.load_texture_from_image(cat_sobel)
cat_gaussian_texture = rl.load_texture_from_image(cat_gaussian)

# Once images have been converted to texture and uploaded to VRAM,
# they can be unloaded from RAM
rl.unload_image(image)
rl.unload_image(cat_gaussian)
rl.unload_image(cat_sobel)
rl.unload_image(cat_sharpened)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_texture(cat_sharpened_texture, 0, 0, rl.WHITE)
    rl.draw_texture(cat_sobel_texture, 200, 0, rl.WHITE)
    rl.draw_texture(cat_gaussian_texture, 400, 0, rl.WHITE)
    rl.draw_texture(texture, 600, 0, rl.WHITE)
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texture)
rl.unload_texture(cat_gaussian_texture)
rl.unload_texture(cat_sobel_texture)
rl.unload_texture(cat_sharpened_texture)

rl.close_window()  # Close window and OpenGL context