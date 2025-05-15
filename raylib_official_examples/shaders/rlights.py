#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# raylib.lights - Some useful functions to deal with lights data in Python, used by multiple examples.
#
# LICENSE: zlib/libpng
#
# Copyright (c) 2017-2025 Victor Fisac (@victorfisac) and Ramon Santamaria (@raysan5)
# Ported to Python by GitHub Copilot, 2025
#
# This software is provided "as-is", without any express or implied warranty. In no event
# will the authors be held liable for any damages arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose, including commercial
# applications, and to alter it and redistribute it freely, subject to the following restrictions:
#
#   1. The origin of this software must not be misrepresented; you must not claim that you
#   wrote the original software. If you use this software in a product, an acknowledgment
#   in the product documentation would be appreciated but is not required.
#
#   2. Altered source versions must be plainly marked as such, and must not be misrepresented
#   as being the original software.
#
#   3. This notice may not be removed or altered from any source distribution.

import pyray as rl

# Max dynamic lights supported by shader
MAX_LIGHTS = 4

# Light types
LIGHT_DIRECTIONAL = 0
LIGHT_POINT = 1

# Global variable to keep track of the number of lights
lights_count = 0

class Light:
    def __init__(self):
        self.type = 0
        self.enabled = True
        self.position = rl.Vector3(0, 0, 0)
        self.target = rl.Vector3(0, 0, 0)
        self.color = rl.Color(0, 0, 0, 255)
        self.attenuation = 0.0
        
        # Shader locations
        self.enabled_loc = 0
        self.type_loc = 0
        self.position_loc = 0
        self.target_loc = 0
        self.color_loc = 0
        self.attenuation_loc = 0

def create_light(light_type, position, target, color, shader):
    """Create a light and get shader locations"""
    global lights_count
    
    light = Light()
    
    if lights_count < MAX_LIGHTS:
        light.enabled = True
        light.type = light_type
        light.position = position
        light.target = target
        light.color = color
        
        # NOTE: Lighting shader naming must be the provided ones
        light.enabled_loc = rl.get_shader_location(shader, f"lights[{lights_count}].enabled")
        light.type_loc = rl.get_shader_location(shader, f"lights[{lights_count}].type")
        light.position_loc = rl.get_shader_location(shader, f"lights[{lights_count}].position")
        light.target_loc = rl.get_shader_location(shader, f"lights[{lights_count}].target")
        light.color_loc = rl.get_shader_location(shader, f"lights[{lights_count}].color")
        
        update_light_values(shader, light)
        
        lights_count += 1
    
    return light

def update_light_values(shader, light):
    """Send light properties to shader"""
    # Send to shader light enabled state and type
    rl.set_shader_value(shader, light.enabled_loc, rl.ffi.new("int *", light.enabled), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, light.type_loc, rl.ffi.new("int *", light.type), rl.SHADER_UNIFORM_INT)
    
    # Send to shader light position values
    position = rl.ffi.new("float[3]", [light.position.x, light.position.y, light.position.z])
    rl.set_shader_value(shader, light.position_loc, position, rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light target position values
    target = rl.ffi.new("float[3]", [light.target.x, light.target.y, light.target.z])
    rl.set_shader_value(shader, light.target_loc, target, rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light color values
    color = rl.ffi.new("float[4]", [
        light.color[0]/255.0,
        light.color[1]/255.0,
        light.color[2]/255.0,
        light.color[3]/255.0
    ])
    rl.set_shader_value(shader, light.color_loc, color, rl.SHADER_UNIFORM_VEC4)
