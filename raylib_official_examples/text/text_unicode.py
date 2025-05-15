"""raylib [text] example - Unicode
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 2.5, last time updated with raylib 4.0
Example contributed by Vlad Adrian (@demizdor) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Vlad Adrian (@demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

# Define constants
EMOJI_PER_WIDTH = 8
EMOJI_PER_HEIGHT = 4

# String containing 180 emoji codepoints
emoji_codepoints = [
    "🌀", "😀", "😂", "🤣", "😃", "😆", "😉", "😋", "😎", "😍", "😘", "😗", "😙", "😚", "🙂", "🤗", "🤩", "🤔", "🤨", "😐", "😑",
    "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "😴", "😌", "😛", "😜", "🤤", "😒", "😕", "🙃", "🤑", "😲", "🙁",
    "😖", "😞", "😟", "😤", "😢", "😭", "😦", "😩", "🤯", "😬", "😰", "😱", "😳", "🤪", "😵", "😡", "😠", "🤬", "😷", "🤒", "🤕",
    "🤢", "🤮", "🤧", "😇", "🤠", "🤫", "🤭", "🧐", "🤓", "😈", "👿", "👹", "👺", "💀", "👻", "👽", "👾", "🤖", "💩", "😺", "😸",
    "😹", "😻", "😽", "🙀", "😿", "🌾", "🌿", "🍀", "🍃", "🍇", "🍓", "🥝", "🍅", "🥥", "🍑", "🥕", "🍆", "🥔", "🥥", "🌽", "🌶",
    "🥒", "🥦", "🍄", "🥜", "🌰", "🍞", "🥐", "🥖", "🥨", "🥞", "🧀", "🍖", "🍗", "🥩", "🥓", "🍔", "🍟", "🍕", "🌭", "🥪", "🌮",
    "🌯", "🥙", "🥚", "🍳", "🥘", "🍲", "🥣", "🥗", "🍿", "🥫", "🍱", "🍘", "🍝", "🍠", "🍢", "🍥", "🍡", "🥟", "🥠", "🍦", "🍪",
    "🎂", "🍰", "🥧", "🍫", "🍯", "🍼", "🥛", "🍵", "🍶", "🍾", "🍷", "🍻", "🥂", "🥃", "🥤", "🥢", "👁", "👅", "👄", "💋", "💘",
    "💓", "💗", "💙", "💛", "🧡", "💜", "🖤", "💝", "💟", "💌", "💢", "💣"
]

# Array containing multilingual messages
messages = [
    {"text": "Falsches Üben von Xylophonmusik quält jeden größeren Zwerg", "language": "German"},
    {"text": "Beiß nicht in die Hand, die dich füttert.", "language": "German"},
    {"text": "Außerordentliche Übel erfordern außerordentliche Mittel.", "language": "German"},
    {"text": "Կրնամ ապակի ուտել և ինծի անհանգիստ չըներ", "language": "Armenian"},
    {"text": "Երբ որ կացինը եկաւ անտառ, ծառերը ասացին... «Կոտը մերոնցից է:»", "language": "Armenian"},
    {"text": "Գառը՝ գարնան, ձիւնը՝ ձմռան", "language": "Armenian"},
    {"text": "Jeżu klątw, spłódź Finóm część gry hańb!", "language": "Polish"},
    {"text": "Dobrymi chęciami jest piekło wybrukowane.", "language": "Polish"},
    {"text": "Îți mulțumesc că ai ales raylib.\nȘi sper să ai o zi bună!", "language": "Romanian"},
    {"text": "Эх, чужак, общий съём цен шляп (юфть) вдрызг!", "language": "Russian"},
    {"text": "Я люблю raylib!", "language": "Russian"},
    {"text": "Молчи, скрывайся и таи\nИ чувства и мечты свои –\nПускай в душевной глубине\nИ всходят и зайдут оне\nКак звезды ясные в ночи-\nЛюбуйся ими – и молчи.", "language": "Russian"},
    {"text": "Voix ambiguë d'un cœur qui au zéphyr préfère les jattes de kiwi", "language": "French"},
    {"text": "Benjamín pidió una bebida de kiwi y fresa; Noé, sin vergüenza, la más exquisita champaña del menú.", "language": "Spanish"},
    {"text": "Ταχίστη αλώπηξ βαφής ψημένη γη, δρασκελίζει υπέρ νωθρού κυνός", "language": "Greek"},
    {"text": "Η καλύτερη άμυνα είναι η επίθεση.", "language": "Greek"},
    {"text": "Χρόνια και ζαμάνια!", "language": "Greek"},
    {"text": "Πώς τα πας σήμερα;", "language": "Greek"},
    {"text": "我能吞下玻璃而不伤身体。", "language": "Chinese"},
    {"text": "你吃了吗？", "language": "Chinese"},
    {"text": "不作不死。", "language": "Chinese"},
    {"text": "最近好吗？", "language": "Chinese"}
]

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_WINDOW_HIGHDPI)
    rl.init_window(screen_width, screen_height, "raylib [text] example - Unicode")

    # Default font already supports a certain number of Unicode codepoints (depending on platform)
    font_default = rl.get_font_default()
    
    # Load NotoSans-Regular.ttf which supports multiple languages 
    # (it can also be downloaded directly from Google Fonts)
    font_symbols = rl.load_font(str(THIS_DIR/"resources/noto_cjk.fnt"))
    
    # Setup scrolling variables
    message_index = 0
    emoji_page_index = 0
    frame_counter = 0
    position_y = screen_height - 100.0
    
    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        frame_counter += 1
        
        # Scroll up
        position_y -= 1.0
        
        # Reset scrolling and change message when required
        if (position_y < -300.0):
            position_y = screen_height - 100.0
            message_index += 1
            if message_index >= len(messages):
                message_index = 0
            
        # Change emoji page
        if rl.is_key_pressed(rl.KEY_RIGHT):
            emoji_page_index += 1
            if emoji_page_index > 4:
                emoji_page_index = 0
        elif rl.is_key_pressed(rl.KEY_LEFT):
            emoji_page_index -= 1
            if emoji_page_index < 0:
                emoji_page_index = 4
        
        # Draw
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        # Draw current selected emoji page
        for i in range(EMOJI_PER_HEIGHT):
            for j in range(EMOJI_PER_WIDTH):
                pos = emoji_page_index*EMOJI_PER_HEIGHT*EMOJI_PER_WIDTH + i*EMOJI_PER_WIDTH + j
                if pos < len(emoji_codepoints):
                    # WARNING: When drawing text with a custom font, codepoints are directly mapped to font glyphs,
                    # so maybe some emojis could fall into non-supported glyphs codepoints range 
                    # and you will see the default font character
                    rl.draw_text(emoji_codepoints[pos], 20 + j*60, 20 + i*60, 50, rl.LIGHTGRAY)
        
        # Draw current message
        current_message = messages[message_index]["text"]
        language = messages[message_index]["language"]
        
        rl.draw_text(f"Message ({language}):", 40, (position_y - 30), 20, rl.DARKGRAY)
        
        # Draw the message using the appropriate font
        text_y_pos = position_y
        for line in current_message.split("\n"):
            rl.draw_text_ex(font_symbols, line, rl.Vector2(40, text_y_pos), 24, 2, rl.BLACK)
            text_y_pos += 24  # Move down for next line
        
        # Draw info
        rl.draw_rectangle(0, screen_height - 66, screen_width, 66, rl.SKYBLUE)
        rl.draw_text_ex(font_default, "Use LEFT/RIGHT keys to change emoji page", rl.Vector2(40, screen_height - 30), 20, 2, rl.WHITE)
        
        # Draw page indicator
        rl.draw_text(f"EMOJI PAGE: {emoji_page_index + 1}/5", screen_width - 160, screen_height - 30, 20, rl.WHITE)
        
        rl.end_drawing()
        
    # De-Initialization
    rl.unload_font(font_symbols)  # Unload font
    
    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()