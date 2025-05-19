Some notes about pyray API that should be looked into as they seem clumsy to use:

- pyray.YELLOW is a tuple. Should be a namedtuple for convenience, so we could use .r, .g ...
There is also places where an rl.Color type is expected, and pyray.YELLOW is not a rl.Color instance.

- style can returns negative int32 value for color, but color only accept uint32.
- rl.set_shader_value() only accept a pointer for the value which make it very painful/verbose to use

