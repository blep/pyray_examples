List of examples with issues.

The template for the issues is:
- example_path: [optional action required to reproduce the issue]
  [optional line of code with the issue]
  Exception message


audio/:
- raylib_py_examples/audio/audio_mixed_processor.py: TypeError: initializer for ctype 'void(*)(void *, unsigned int)' must be a cdata pointer, not function
- raylib_py_examples/audio/audio_raw_stream.py:
  rl.set_audio_stream_callback(stream, audio_input_callback)
  TypeError: initializer for ctype 'void(*)(void *, unsigned int)' must be a cdata pointer, not function
- raylib_py_examples/audio/audio_sound_positioning.py: TypeError: _make_struct_constructor_function.<locals>.func() got an unexpected keyword argument 'position'
- raylib_py_examples/audio/audio_stream_effects.py: Pressd key D or F: TypeError: initializer for ctype 'void(*)(void *, unsigned int)' must be a cdata pointer, not CFunctionType

 core/:
- raylib_py_examples/core/core_3d_camera_first_person.py: Press P key => AttributeError: module 'pyray' has no attribute 'camera_yaw'
- raylib_py_examples/core/core_automation_events.py: AttributeError: module 'pyray' has no attribute 'load_automation_events'
- raylib_py_examples/core/core_custom_frame_control.py: AttributeError: module 'pyray' has no attribute 'get_target_fps'
- raylib_py_examples/core/core_custom_logging.py: rl.set_trace_log_callback(custom_log), TypeError: initializer for ctype 'void(*)(int, char *, void *)' must be a cdata pointer, not CFunctionType
- raylib_py_examples/core/core_drop_files.py: from raylib.defines import MAX_FILEPATH_SIZE
- raylib_py_examples/core/core_drop_files.py:
  - from raylib.defines import MAX_FILEPATH_SIZE: not defined  
  - dropped filenames displayed as "CDATA * char", instead of actual filenames
- raylib_py_examples/core/core_storage_values.py: 
  - AttributeError: module 'pyray' has no attribute 'save_storage_value'
  - AttributeError: module 'pyray' has no attribute 'load_storage_value'
- raylib_py_examples/core/core_vr_simulator.py: TypeError: _make_struct_constructor_function.<locals>.func() got an unexpected keyword argument 'h_resolution'

gui/:
- raylib_py_examples/gui/animation_curve.py:
  rl.ColorAlpha(rl.RED, 0.9)
  AttributeError: module 'pyray' has no attribute 'ColorAlpha'
- raylib_py_examples/gui/gui_value_box_float.py:
  pressed = rl.gui_text_box_ex(bounds, text_value, 64, edit_mode)
  AttributeError: module 'pyray' has no attribute 'gui_text_box_ex'
- raylib_py_examples/gui/controls_test_suite.py: click on "Default" button (botttom-left) to change style 
  rl.gui_load_style_jungle()
  AttributeError: module 'pyray' has no attribute 'gui_load_style_jungle'
  Notes: all gui_load_style_*() functions seems to be missing (or are somewhere else)
- raylib_py_examples/gui/image_exporter.py:
  texture = rl.Texture2D()
  ffi.error: undefined struct/union name: struct Texture2D *
- raylib_py_examples/gui/floating_window.py:
  rl.gui_load_style_dark()
  AttributeError: module 'pyray' has no attribute 'gui_load_style_dark'
- raylib_py_examples/gui/custom_sliders.py:  AttributeError: module 'pyray' has no attribute 'gui_draw_rectangle'
- raylib_py_examples/gui/custom_file_dialog.py:
  texture = rl.Texture2D()
  ffi.error: undefined struct/union name : struct Texture2D *
- raylib_py_examples/gui/custom_input_box.py:
  pressed = rl.gui_text_box_ex(bounds, text_value, RAYGUI_VALUEBOX_MAX_CHARS, edit_mode)
  AttributeError: module 'pyray' has no attribute 'gui_text_box_ex'
- raylib_py_examples/gui/image_importer_raw.py:
  texture = rl.Texture2D()
  ffi.error: undefined struct/union name : struct Texture2D *
- raylib_py_examples/gui/property_list.py:
  bounds.y + (i * item_height) - scroll_ptr[0],
  TypeError: unsupported operand type(s) for -: 'float' and '_cffi_backend.__CDataOwn'
- raylib_py_examples/gui/style_selector.py:
  rl.gui_load_style_bluish()
  AttributeError: module 'pyray' has no attribute 'gui_load_style_bluish'

models/:
- raylib_py_examples/models/models_skybox.py: 
  rl.set_shader_value(
        skybox.materials[0].shader, 
        rl.get_shader_location(skybox.materials[0].shader, "environmentMap"), 
        rl.MATERIAL_MAP_CUBEMAP,   # <== complains about that 
        rl.SHADER_UNIFORM_INT
    )
  TypeError: Argument 2 (7) must be a cdata pointer. Type is void so I don't know what type it should be.If it's a const string you can create it with pyray.ffi.new('char []', b"whatever") . If it's a float you can create it with pyray.ffi.new('float *', 1.0)
  => most common use cas is passing constant, IMHO, binding should allow it
- raylib_py_examples/models/models_loading_vox.py:
  rl.set_shader_value(shader, ambient_loc, [0.1, 0.1, 0.1, 1.0], rl.SHADER_UNIFORM_VEC4)
  TypeError: Argument 2 ([0.1, 0.1, 0.1, 1.0]) must be a cdata pointer. Type is void so I don't know what type it should be.If it's a const string you can create it with pyray.ffi.new('char []', b"whatever") . If it's a float you can create it with pyray.ffi.new('float *', 1.0)
- raylib_py_examples/models/models_mesh_generation.py:
  mesh.vertices = vertices
  TypeError: initializer for ctype 'float *' must be a cdata pointer, not list
- raylib_py_examples/models/models_point_rendering.py:
  mesh.vertices = vertices
  TypeError: initializer for ctype 'float *' must be a cdata pointer, not list

others/:
- raylib_py_examples/others/easings_testbed.py: AttributeError: module 'pyray' has no attribute 'ease_linear_none'
- raylib_py_examples/others/embedded_files_loading.py: 
  # In the C version, these are loaded from header files
  # In our Python version, we'll load from actual files instead
  others\..\resources\country.mp3] Failed to open file
  => IMHO, don't think this feature make sense in python. But a pyinstaller or the like example would make sense
- raylib_py_examples/others/rlgl_standalone.py:
  rotation = rl.Quaternion(0.0, 0.0, 0.0, 1.0)
  ffi.error: undefined struct/union name : struct Quaternion *
- raylib_py_examples/others/raylib_opengl_interop.py:
  glBindVertexArray(vao)
  OpenGL.error.GLError: GLError(
	err = 1282,
	description = b'op\xe9ration non valide',
	baseOperation = glBindVertexArray,
	cArguments = (np.uint32(2),)
  )
  => Notes: might just be because I running on an insanely old NVidia GeForce 750

shaders/:
- raylib_py_examples/shaders/shaders_deferred_render.py: Press key 1 (switch G buffer)
  texture = rl.Texture2D()
  ffi.error: undefined struct/union name : struct Texture2D *
- raylib_py_examples/shaders/shaders_hybrid_render.py:
  target = rl.RenderTexture2D()
  ffi.error: undefined struct/union name: struct RenderTexture2D *
- raylib_py_examples/shaders/shaders_lightmap.py, 
  raylib_py_examples/shaders/shaders_mesh_instancing.py:
  mesh_texcoords2_ptr = rl.rl_malloc(mesh.vertexCount * 2 * ctypes.sizeof(rl.ffi.new("float *", 0))) 
  AttributeError: module 'pyray' has no attribute 'rl_malloc'
  => Notes: very low-level memory manipulation. Deep dive required to see how to adadpt to Python
- raylib_py_examples/shaders/shaders_shadowmap.py:
  target = rl.RenderTexture2D()
  ffi.error: undefined struct/union name: struct RenderTexture2D *
- raylib_py_examples/shaders/shaders_view_depth.py:
  target = rl.RenderTexture2D()
  ffi.error: undefined struct/union name : struct RenderTexture2D *
- raylib_py_examples/shaders/shaders_write_depth.py:
  target = rl.RenderTexture2D()
  ffi.error: undefined struct/union name : struct RenderTexture2D *

shapes/:
- raylib_py_examples/shapes/shapes_easings_ball_anim.py,
  raylib_py_examples/shapes/shapes_easings_box_anim.py,
  raylib_py_examples/shapes/shapes_easings_rectangle_array.py:
  AttributeError: module 'pyray' has no attribute 'ease_elastic_out'
- raylib_py_examples/shapes/shapes_rectangle_advanced.py:
    draw_rectangle_rounded_gradient_h(rec, 0.8, 0.8, 36, rl.BLUE, rl.RED)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "E:\prg\prj\puzzlator-py-raylib\raylib_py_examples\shapes\shapes_rectangle_advanced.py", line 119, in draw_rectangle_rounded_gradient_h
    rl.rl_color4ub(color.r, color.g, color.b, color.a)
                   ^^^^^^^
  AttributeError: 'tuple' object has no attribute 'r'
- raylib_py_examples/shapes/shapes_splines_drawing.py:
   if rl.gui_dropdown_box(rl.Rectangle(12, 8 + 24, 140, 28), "LINEAR;BSPLINE;CATMULLROM;BEZIER", spline_type_active_ptr, spline_type_edit_mode_ptr):
  TypeError: int() not supported on cdata '_Bool *'
- raylib_py_examples/shapes/shapes_top_down_lights.py:
  => shadows are buggy. Likely comes from bad conversion of: (quickly fixed 2 invalid python code)
  vertices = lights[slot].shadows[i].vertices

text/:
- raylib_py_examples/text/text_draw_3d.py
  => no text is drawn
- raylib_py_examples/text/text_codepoints_loading.py:
  font = rl.load_font_ex(str(THIS_DIR/"resources/DotGothic16-Regular.ttf"), 36, codepoints_array, codepoints_no_dups_count)
  TypeError: initializer for ctype 'int *' must be a pointer to same type, not cdata 'int(*)[]'
- raylib_py_examples/text/text_raylib_fonts.py: all fonts displayed the bottom instead of behind vertical aligned.
- [text_rectangle_bounds.py](text/text_rectangle_bounds.py):
  rl.draw_text_rec(font, text, rec, font_size, spacing, word_wrap, tint)
  AttributeError: module 'pyray' has no attribute 'draw_text_rec'
- raylib_py_examples/text/text_unicode.py:
  rl.draw_text(f"Message ({language}):", 40, (position_y - 30), 20, rl.DARKGRAY)
  TypeError: an integer is required

textures/:
- raylib_py_examples/textures/textures_bunnymark.py: doesn't display any bunny. Bunny counter doesn't go up.
- raylib_py_examples/textures/textures_image_kernel.py:
  sharpen_kernel = normalize_kernel(sharpen_kernel, 9)
  # ...
  rl.image_kernel_convolution(cat_sharpened, sharpen_kernel, 9)
  TypeError: Argument 1 ([0.0, -1.0, 0.0, -1.0, 5.0, -1.0, 0.0, -1.0, 0.0]) must be a ctype float, please create one with: pyray.ffi.new('float *', 1.0)
- raylib_py_examples/textures/textures_sprite_explosion.py: nothing displayed, no audio
