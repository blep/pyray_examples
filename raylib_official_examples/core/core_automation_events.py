"""raylib [core] example - automation events
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example based on 2d_camera_platformer example by arvyy (@arvyy)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import ctypes # Required for AutomationEventList interaction
import math

# Constants
GRAVITY = 400.0
PLAYER_JUMP_SPD = 350.0
PLAYER_HOR_SPD = 200.0
MAX_ENVIRONMENT_ELEMENTS = 5
FIXED_DELTA_TIME = 0.015  # As used in the C example

# Player class
class Player:
    def __init__(self, position: rl.Vector2, speed: float, can_jump: bool):
        self.position = position
        self.speed = speed
        self.can_jump = can_jump

# Environment Element class
class EnvElement:
    def __init__(self, rect: rl.Rectangle, blocking: int, color: rl.Color):
        self.rect = rect
        self.blocking = blocking
        self.color = color

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - automation events")

    # Define player
    player = Player(rl.Vector2(400, 280), 0, False)

    # Define environment elements (platforms)
    env_elements = [
        EnvElement(rl.Rectangle(0, 0, 1000, 400), 0, rl.LIGHTGRAY),
        EnvElement(rl.Rectangle(0, 400, 1000, 200), 1, rl.GRAY),
        EnvElement(rl.Rectangle(300, 200, 400, 10), 1, rl.GRAY),
        EnvElement(rl.Rectangle(250, 300, 100, 10), 1, rl.GRAY),
        EnvElement(rl.Rectangle(650, 300, 100, 10), 1, rl.GRAY)
    ]

    # Define camera
    camera = rl.Camera2D()
    camera.target = player.position
    camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    # Automation events
    # Create an empty list structure. load_automation_events(None) is specific to pyray for this.
    aelist = rl.load_automation_events(None) 
    # Tell raylib to record into this list instance if recording starts.
    # We pass it by reference using ctypes.byref().
    rl.set_automation_event_list(ctypes.byref(aelist))
    
    event_recording = False
    event_playing = False
    
    # frame_counter in C example was for event recording/playing timing, not global frames.
    # Let's rename to avoid confusion with a general frame counter if we add one.
    automation_frame_counter = 0 
    play_event_index = 0 # Index for the event currently being played from aelist

    rl.set_target_fps(60)

    while not rl.window_should_close():
        delta_time = FIXED_DELTA_TIME # Use fixed delta time as in C example

        # Dropped files logic
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()
            if dropped_files.count > 0:
                # Check only the first dropped file
                filepath = rl.ensure_str(dropped_files.paths[0])
                if rl.is_file_extension(filepath, ".txt") or rl.is_file_extension(filepath, ".rae"):
                    if aelist.events: # If aelist was previously loaded or recorded into
                        rl.unload_automation_event_list(aelist) # Unload old events
                    
                    aelist = rl.load_automation_events(filepath.encode('utf-8')) # Load new list
                    # rl.set_automation_event_list(ctypes.byref(aelist)) # Not needed again unless we intend to record into the newly loaded list
                    
                    event_recording = False
                    event_playing = True
                    automation_frame_counter = 0 
                    play_event_index = 0
                    
                    # Reset scene state to play
                    player.position = rl.Vector2(400, 280)
                    player.speed = 0
                    player.can_jump = False
                    camera.target = player.position
                    camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)
                    camera.rotation = 0.0
                    camera.zoom = 1.0
                    
                    rl.trace_log(rl.LOG_INFO, f"Successfully loaded automation events from: {filepath}")

            rl.unload_dropped_files(dropped_files)

        # Update player
        if rl.is_key_down(rl.KEY_LEFT):
            player.position.x -= PLAYER_HOR_SPD * delta_time
        if rl.is_key_down(rl.KEY_RIGHT):
            player.position.x += PLAYER_HOR_SPD * delta_time
        if rl.is_key_down(rl.KEY_SPACE) and player.can_jump:
            player.speed = -PLAYER_JUMP_SPD
            player.can_jump = False

        hit_obstacle = False
        for element in env_elements:
            if element.blocking:
                # Check collision with platform logic (simplified for player's bottom center point)
                player_bottom_x = player.position.x
                player_next_y = player.position.y + player.speed * delta_time
                
                if (element.rect.x <= player_bottom_x <= element.rect.x + element.rect.width and
                    element.rect.y >= player.position.y and # Player is above or at platform level
                    element.rect.y <= player_next_y):      # Player will be at or below platform level
                    
                    hit_obstacle = True
                    player.speed = 0.0
                    player.position.y = element.rect.y # Snap to platform
                    break 

        if not hit_obstacle:
            player.position.y += player.speed * delta_time
            player.speed += GRAVITY * delta_time
            player.can_jump = False
        else:
            player.can_jump = True

        if rl.is_key_pressed(rl.KEY_R): # Reset game
            player.position = rl.Vector2(400, 280)
            player.speed = 0
            player.can_jump = False
            camera.target = player.position
            camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)
            camera.rotation = 0.0
            camera.zoom = 1.0
            automation_frame_counter = 0
            play_event_index = 0
            # event_playing = False # Optionally stop playing on reset

        # Events playing
        if event_playing and aelist.events and aelist.count > 0:
            # Multiple events could be on the same frame
            while play_event_index < aelist.count and \
                  aelist.events[play_event_index].frame == automation_frame_counter:
                
                rl.trace_log(rl.LOG_INFO, f"Playing event: frame {aelist.events[play_event_index].frame}, type {aelist.events[play_event_index].type}")
                rl.play_automation_event(aelist.events[play_event_index])
                play_event_index += 1

                if play_event_index >= aelist.count:
                    event_playing = False
                    play_event_index = 0
                    # automation_frame_counter = 0 # Reset counter or let it continue? C example resets.
                    rl.trace_log(rl.LOG_INFO, "FINISH PLAYING AUTOMATION EVENTS!")
                    break 
            
            if event_playing: # If still playing after processing current frame's events
                 automation_frame_counter += 1


        # Update camera
        camera.target = player.position
        # Mouse wheel zoom (check if event playing might affect this)
        # The C example applies mouse wheel AFTER potential event playing for the frame.
        # If an event sets mouse wheel, GetMouseWheelMove will pick it up.
        camera.zoom += rl.get_mouse_wheel_move() * 0.05
        if camera.zoom > 3.0: camera.zoom = 3.0
        elif camera.zoom < 0.25: camera.zoom = 0.25

        # Camera clamping (simplified version from C example)
        # This part needs careful translation if full C logic is required.
        # For now, a simpler target following is implemented.
        # The C example's camera bounding is more complex, ensuring all env elements are visible.
        # Simplified:
        camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)


        # Event management (Recording/Playing Toggle)
        if rl.is_key_pressed(rl.KEY_S):  # Toggle events recording
            if not event_playing: # Can't record if playing
                if event_recording: # Stop recording
                    rl.stop_automation_event_recording()
                    event_recording = False
                    if aelist.count > 0:
                         rl.export_automation_event_list(aelist, b"automation.rae")
                         rl.trace_log(rl.LOG_INFO, f"STOPPED RECORDING. Events recorded: {aelist.count}. Saved to automation.rae")
                    else:
                         rl.trace_log(rl.LOG_INFO, "STOPPED RECORDING. No events recorded.")
                else: # Start recording
                    # If there's an existing list (e.g. loaded), clear it before new recording?
                    # C example implies StartAutomationEventRecording reuses/clears the list set by SetAutomationEventList.
                    # We might need to re-initialize aelist or ensure it's clean.
                    # For safety, let's unload if it has events, then re-init for recording.
                    if aelist.events:
                        rl.unload_automation_event_list(aelist)
                    aelist = rl.load_automation_events(None) # Get a fresh, empty list
                    rl.set_automation_event_list(ctypes.byref(aelist)) # Point raylib to the new list

                    rl.set_automation_event_base_frame(automation_frame_counter) # C example used 180, here using current for flexibility
                    rl.start_automation_event_recording()
                    event_recording = True
                    automation_frame_counter = 0 # Reset for recording duration
                    rl.trace_log(rl.LOG_INFO, "STARTED RECORDING EVENTS...")

        elif rl.is_key_pressed(rl.KEY_A): # Toggle events playing
            if not event_recording and aelist.events and aelist.count > 0:
                if event_playing: # If playing, stop/pause (C example doesn't have pause, just restarts play)
                    event_playing = False
                    automation_frame_counter = 0
                    play_event_index = 0
                    rl.trace_log(rl.LOG_INFO, "STOPPED PLAYING (manual toggle).")
                else: # Start playing
                    event_playing = True
                    automation_frame_counter = 0 
                    play_event_index = 0
                    
                    # Reset scene state to play
                    player.position = rl.Vector2(400, 280)
                    player.speed = 0
                    player.can_jump = False
                    camera.target = player.position
                    camera.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0)
                    camera.rotation = 0.0
                    camera.zoom = 1.0
                    rl.trace_log(rl.LOG_INFO, f"STARTED PLAYING {aelist.count} EVENTS...")
            elif not event_recording and (not aelist.events or aelist.count == 0):
                 rl.trace_log(rl.LOG_INFO, "No events to play. Record (S) or drop a .rae file.")


        if event_recording : # Only increment if actively recording new events
            automation_frame_counter +=1
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.LIGHTGRAY)

        rl.begin_mode_2d(camera)
        for element in env_elements:
            rl.draw_rectangle_rec(element.rect, element.color)
        
        # Draw player as a rectangle
        player_rect = rl.Rectangle(player.position.x - 20, player.position.y - 40, 40, 40)
        rl.draw_rectangle_rec(player_rect, rl.RED)
        rl.end_mode_2d()

        # UI Text
        rl.draw_rectangle(10, 10, 320, 155, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(10, 10, 320, 155, rl.fade(rl.BLUE, 0.8))

        rl.draw_text("Controls:", 20, 20, 10, rl.BLACK)
        rl.draw_text("- Arrows to move, Space to jump", 30, 40, 10, rl.DARKGRAY)
        rl.draw_text("- R to reset game", 30, 55, 10, rl.DARKGRAY)
        rl.draw_text("- S to Start/Stop recording events", 30, 70, 10, rl.DARKGRAY)
        rl.draw_text("- A to Play/Stop recorded/loaded events", 30, 85, 10, rl.DARKGRAY)
        rl.draw_text("- Drag & Drop .rae/.txt event file to load", 30, 100, 10, rl.DARKGRAY)

        status_text = "IDLE"
        status_color = rl.BLACK
        if event_recording:
            status_text = f"RECORDING (Frame: {automation_frame_counter})"
            status_color = rl.RED
        elif event_playing:
            status_text = f"PLAYING (Frame: {automation_frame_counter}, Event: {play_event_index}/{aelist.count if aelist else 0})"
            status_color = rl.LIME
        
        rl.draw_text(status_text, 20, 125, 10, status_color)
        rl.draw_text(f"Events in list: {aelist.count if aelist and aelist.events else 0}", 20, 140, 10, rl.DARKBLUE)
        
        rl.draw_fps(screen_width - 90, 10)
        rl.end_drawing()

    # De-Initialization
    if aelist.events: # Check if aelist has been populated before unloading
        rl.unload_automation_event_list(aelist)
    rl.close_window()

if __name__ == '__main__':
    main()
