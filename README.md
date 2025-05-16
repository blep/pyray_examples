# 100+ python examples for pyray, the python bindings of raylib

This repo contains example programs for [pyray](https://github.com/electronstudio/raylib-python-cffi), the Python 
bindings for the [raylib](https://github.com/raysan5/raylib) library. All examples have been migrated from the 
official raylib C examples.

Original C examples:
- [raylib](https://github.com/raysan5/raylib/tree/master/examples)
- [raylib GUI](https://github.com/raysan5/raygui/tree/master/examples)

> **Note:**  
> A ticket was opened to request integration of these examples with pyray:  
> https://github.com/electronstudio/raylib-python-cffi/issues/173

## Running the examples

Create a virtual environment (for Windows, activation differs on each platform):
```bash
python -m venv venv
venv\Scripts\activate
```

Install the pyray package:
```bash
pip install -r requirements.txt
```

Run the desired example:
```bash
python raylib_official_examples/textures/textures_background_scrolling.py
```

## Using those examples

*WARNING*: most of the code is the result of an automatic migration from C to Python using non-deterministic tools, 
so it may contain bugs, may not be idiomatic Python, contains odd comments... 

*Not all the code was reviewed.* (I just don't have the time for that) 

## Example licenses

The license of the original C examples [has been preserved](raylib_official_examples/copyright_comment.py).
(See the module-level docstring in each.) As far as I know, they all follow the zlib/libpng license.

## Examples status

Note that not all examples work: 131/174 (~75%) examples work without issues.

See [migration_issues](raylib_official_examples/migration_issues.md) for the list of examples with known issues, 
and a brief description of the issue. Note that some examples run, but some actions cause crashes. The action is 
described next to the example path.

See [pyray API oddities](raylib_official_examples/pyray_api_oddities.md) for some quick notes on API that seem
clumsy to use.

Many examples share common failures, such as failure to create a Texture2D().

The script [list_working_examples.py](raylib_official_examples/list_working_examples.py) can be used to update:
- [list of examples that work without known issues](raylib_official_examples/examples_list_working.txt)
- [list of examples that have known issues](raylib_official_examples/examples_list_with_issues.txt)

## How this migration from C to Python was done

This is a heavily tool-assisted migration of those 120+ examples, in about 1.5 calendar days.

Tools used (as of 2025-05-14):
- Visual Studio Code (1.100.1), with GitHub Copilot
  - Agent mode
  - Model: mostly "Claude 3.7 Sonnet", but initially used "Gemini 2.5 Pro (Preview)". 
    Unfortunately, Gemini started returning constant "500 Server Error", so I switched to Claude which felt much 
    slower, but gave good results with some rare Python syntax/indent issues...

The original C examples were copied into the repo directory: the Copilot Agent is only allowed to access files within 
the project directory. This is the great advantage of using the agent mode: you don't need to add files to the context,
just provide some reference to them.

You can find a rough [log of the prompts here](prompts/migrate_to_py.md), though midway I started just updating the 
last one as it was growing too big, and it seems to accept new guidelines without issues.

## Main migration prompt

Migration prompts started with the first paragraph, and grew as I found recurrent issues.
Recommendations:
- Create the target directory beforehand if you don't want to waste 1 min for "I need to create the directory".
- Don't trust it when it says it migrated everything. Compare the original number of .c and .py files. It's common
  to require 3+ iterations for a directory (but this also gives you the opportunity to adjust the prompt with newly
  discovered issues).
- In practice, I was testing/tracking down issues on the previous conversion batch while the tool worked on the next
  batch. To track a given source had been tested, I added it to git (which shows up in a different color in PyCharm).
- For some languages, it may be necessary to provide complete examples of "good" quality code. Add these source files 
  to the context and explain in the prompt how they should be used as a reference.  

*Prompt:*
```text
Let's migrate all examples from raylib_c_examples/textures to raylib_official_examples/textures. Existing files may have already been migrated.
Use "import pyray as rl" to import raylib.

Comments must be written in English.

Don't forget that:
- The correct way to call rlgl_* functions in Python is, for example: "rl.rl_push_matrix()".
- It is rl.rl_color4ub(), not rl.rl_color_4ub()
- It is rl.rl_normal3f(), not rl.rl_normal_3f()
- It is rl.draw_texture_n_patch, not rl.draw_texture_npatch()
- It is "rl.update_camera(camera, rl.CAMERA_FREE)", not "rl.update_camera(rl.byref(camera), rl.CAMERA_FREE)", rl.byref() doesn't exist
- It is rl.rl_scalef(), not rl.rl_scale_f()
- It is rl.rl_rotatef(), not rl.rl_rotate_f()
- It is rl.rl_translatef(), not rl.rl_translate_f()
- It is rl.ffi.new(), not rl.pyray.ffi.new()
- It is rl.gui_get_state(), not rl.get_gui_state()

# Converting file loading
When you see code loading files such as: 
music = rl.load_music_stream("raylib_c_examples/audio/resources/country.mp3") # BAD 

Convert them using the following approach: THIS_DIR global constant (just after the import) with directory of the script, 
and then make the path relative to it:

from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent
#...
music = rl.load_music_stream(str(THIS_DIR/"raylib_c_examples/audio/resources/country.mp3")) # GOOD

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
```

## Review and fix prompt

Below is an example of prompts used to fix non-trivial issues discovered after migration was done.

*Prompt:*
```text
Review all the shapes/ migration to Python. The calls to rl.gui_slider_bar(), which have been incorrectly migrated 
from C to Python, and adjust the code so that it is correct. 
The 4th parameter must be a pointer to float created with: "pyray.ffi.new('float *', 1.0)" for example. The float 
pointer value is accessed with pointer[0].

Example of bad code:
    start_angle = 0.0
    print( f"Angle is {start_angle}" )
    start_angle = rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle:.2f}", start_angle, 0, 720)

Example of correct code:
    start_angle_ptr = rl.ffi.new('float *', 0.0)
    print( f"Angle is {start_angle_ptr[0]}" )
    rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle_ptr[0]:.2f}", start_angle_ptr, 0, 720)

There is also an identical issue for rl.gui_check_box(), but concerning the last parameter. Correct it too. 
```
