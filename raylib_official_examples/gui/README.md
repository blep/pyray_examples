# Raylib GUI Examples (Python)

This directory contains Python implementations of the raylib GUI examples, ported from the original C examples.

## Available Examples

1. **animation_curve.py** - Animated object using customizable animation curves
2. **controls_test_suite.py** - Tests all the core raygui controls in a single interface
3. **custom_file_dialog.py** - Implementation of a custom file dialog
4. **custom_input_box.py** - Custom input box control for float values
5. **custom_sliders.py** - Implementation of custom sliders including vertical ones
6. **floating_window.py** - Demonstrates a draggable floating window
7. **gui_value_box_float.py** - Custom value box for float values
8. **image_exporter.py** - A tool for exporting images in different formats
9. **image_importer_raw.py** - A tool for importing raw image data
10. **portable_window.py** - Implementation of a portable window with custom drag controls
11. **property_list.py** - A property management and editing control
12. **scroll_panel.py** - Demonstrates the use of scrollable panels
13. **standalone.py** - Template for using raygui standalone 
14. **style_selector.py** - A tool for changing between different raygui visual styles

## Notes on Implementation

PORT: will need to revist the port of complex GUI examples once we get the basic working. 

Some examples were challenging to migrate due to their complexity:

1. **animation_curve.py** - This is a simplified version of the original C implementation. The original uses a complex custom curve editor module with cubic Hermite spline interpolation. Our Python version provides similar functionality but with simplified curve mathematics.

2. **property_list.py** - This is a reimplementation of the property list concept, but with a more Python-oriented approach. The original C version uses a complex custom module with macros and multiple property types.

3. **standalone.py** - This is a template showing how one might structure a standalone raygui application in Python.

## Using the Examples

1. Make sure you have installed the required dependencies:
   ```
   pip install raylib pyray
   ```

2. Run any example directly:
   ```
   python custom_sliders.py
   ```

## Common Principles Across Examples

1. All examples use `import pyray as rl` for the raylib bindings
2. Pointer handling is done with `rl.ffi.new()` for GUI controls
3. File paths use the `THIS_DIR` variable for loading resources
4. GUI controls follow the Python naming convention with `snake_case`
