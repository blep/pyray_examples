
Migrate raylib example core_2d_camera_mouse_zoom.c from C to python using the raylib package python bindings. 

Clone the directory structure of the C examples into raylib_py_examples, placing this examples in raylib_py_examples/core/core_2d_camera_mouse_zoom.py

--

You didn't correctly translate the rlgl calls. The correct way to call them in python is for example "rl.rl_push_matrix()". Fix the python code.

--
Greats this example if now working.

Let's migrate all examples from raylib_c_examples/core to raylib_py_examples/core.

Then makes sure to run each migrated python example and fix any error that occurs in the virtualenv found in venv/ (we're on Windows).

---

Let's migrate all examples from raylib_c_examples/core to raylib_py_examples/core. Existing files have already been miograted.

Clone the directory structure of the C examples into raylib_py_examples, placing this examples in raylib_py_examples/core/core_2d_camera_mouse_zoom.py

---
Let's migrate all examples from raylib_c_examples/core to raylib_py_examples/core. Existing files have already been migrated.
Uses "import pyray as rl" to import raylib.
Don't forget that the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".

---

Let's migrate all examples from raylib_c_examples/audio to raylib_py_examples/audio. Existing files may have already been migrated.
Uses "import pyray as rl" to import raylib.
Don't forget that the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Converts them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) #GOOD

---

Let's migrate all examples from raylib_c_examples/shaders to raylib_py_examples/shaders. Existing files may have already been migrated.
Uses "import pyray as rl" to import raylib.
Don't forget that the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Converts them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) #GOOD

# Loading shader
You should never pass None as the first parameter to rl.load_shader. The correct way to load a shader is:
shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

--- (Agent, Claude 3.7 Sonnet)

Review your python migrations of shaders, and fix the isue below. 

The correct way to load a shader is:
shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

Many migration pass None instead of "", which cause failure:
shdr_outline = rl.load_shader(None, str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

---

Let's migrate all examples from raylib_c_examples/shapes to raylib_py_examples/shapes. Existing files may have already been migrated.
Uses "import pyray as rl" to import raylib.
Don't forget that the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Converts them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) #GOOD

# Loading shader
You should never pass None as the first parameter to rl.load_shader. The correct way to load a shader is:
shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))


---

Review the calls to rl.gui_slider_bar(), which has been incorrectly migrated from C to python, and adjust the code so that it is correct. 
The 4th parameter must be a pointer to float created with: "pyray.ffi.new('float *', 1.0)" for example. The float pointer value is accessed with pointer[0].

Example of bad code:
    start_angle = 0.0
    print( f"Angle is {start_angle}" )
    start_angle = rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Example of correct code:
    start_angle = pyray.ffi.new('float *', 0.0)
    print( f"Angle is {start_angle[0]}" )
    rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

--- 

Review all the shapes/ migration to Python. The calls to rl.gui_slider_bar(), which has been incorrectly migrated 
from C to python, and adjust the code so that it is correct. 
The 4th parameter must be a pointer to float created with: "pyray.ffi.new('float *', 1.0)" for example. The float 
pointer value is accessed with pointer[0].

Example of bad code:
    start_angle = 0.0
    print( f"Angle is {start_angle}" )
    start_angle = rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Example of correct code:
    start_angle = pyray.ffi.new('float *', 0.0)
    print( f"Angle is {start_angle[0]}" )
    rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

There is also an identical issue for rl.gui_check_box(), but concerning the last parameter. Correct it too. 

---

Let's migrate all examples from raylib_c_examples/text to raylib_py_examples/text. Existing files may have already been migrated.
Uses "import pyray as rl" to import raylib.
Don't forget that the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Converts them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) #GOOD

# Loading shader
You should never pass None as the first parameter to rl.load_shader. The correct way to load a shader is:
shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

# Using rl.gui_slider_bar() and rl.gui_check_box()

In the calls to rl.gui_slider_bar(), the 4th parameter must be a pointer to float created 
with: "pyray.ffi.new('float *', 1.0)" for example. The float pointer value is accessed 
with pointer[0].

Example of bad code:
    start_angle = 0.0
    print( f"Angle is {start_angle}" )
    start_angle = rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Example of correct code:
    start_angle = pyray.ffi.new('float *', 0.0)
    print( f"Angle is {start_angle[0]}" )
    rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Similar care is required for rl.gui_check_box(), but concerning the last parameter. 


Incorrect: font.base_size, font_sdf.glyph_count
Correct: font.baseSize, font_sdf.glyphCount

----

Let's migrate all examples from raylib_c_examples/textures to raylib_py_examples/textures. Existing files may have already been migrated.
Uses "import pyray as rl" to import raylib.

Comments must be written in english.

Don't forget that:
- the correct way to call rlgl_* functions in python is for example: "rl.rl_push_matrix()".
- It is rl.rl_color4ub(), not rl.rl_color_4ub()
- It is rl.rl_normal3f(), not rl.rl_normal_3f()
- It is rl.draw_texture_n_patch, not rl.draw_texture_npatch()
- It is "rl.update_camera(camera, rl.CAMERA_FREE)", not "rl.update_camera(rl.byref(camera), rl.CAMERA_FREE)", rl.byref() doesn't exist
- It is rl.rl_scalef(), not rl.rl_scale_f()
- It is rl.rl_rotatef(), not rl.rl_rotate_f()
- It is rl.rl_translatef(), not rl.rl_translate_f()
- It is rl.ffi.new(), not rl.pyray.ffi.new()
- It is rl.gui_get_state(), not rl.get_gui_state()
- It is rl.Texture(), not rl.Texture2D() 
- It is rl.RenderTexture(), not rl.RenderTexture2D()

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Converts them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) #GOOD

# Loading shader
You should never pass None as the first parameter to rl.load_shader. The correct way to load a shader is:
shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

# Pointer handling in rl.gui_*() functions

In the calls to rl.gui_slider_bar(), the 4th parameter must be a pointer to float created 
with: "pyray.ffi.new('float *', 1.0)" for example. The float pointer value is accessed 
with pointer[0].

Variables initialized with pyray.ffi.new() must be suffixed with _ptr.  

Example of bad code:
    start_angle = 0.0
    print( f"Angle is {start_angle}" )
    start_angle = rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Example of correct code:
    start_angle_ptr = pyray.ffi.new('float *', 0.0)
    print( f"Angle is {start_angle_ptr[0]}" )
    rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle_ptr, 0, 720)

Similar care is required for rl.gui_check_box(), but concerning the last parameter.
Similar care is required for rl.gui_spinner(), rl.gui_combo_box(), rl.gui_list_view(), rl.gui_list_view() 
and rl.gui_value_box(), but for the 3rd parameter.
Similar care is required for rl.gui_list_view_ex(), but concerning the last 3 parameters.

Incorrect: font.base_size, font_sdf.glyph_count
Correct: font.baseSize, font_sdf.glyphCount
