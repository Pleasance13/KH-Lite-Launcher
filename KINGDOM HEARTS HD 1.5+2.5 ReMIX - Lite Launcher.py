import pygame
import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import tkinter.filedialog
import sys
import subprocess
import tkinter.messagebox
import time

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Function to play sound
def play_sound(sound_file):
    try:
        sound_path = os.path.join(os.path.dirname(__file__), sound_file)
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to scale elements based on the window size
def scale_dimension(original, original_resolution, new_resolution):
    return int(original * (new_resolution[0] / original_resolution[0]))

def safe_quit():
    """Safely quit the application."""
    try:
        root.destroy()  # Destroy all tkinter elements
    except Exception as e:
        print(f"Error during root.destroy: {e}")
    finally:
        sys.exit()  # Ensure the program terminates

# Initialize window
root = tk.Tk()
root.title("KINGDOM HEARTS HD 1.5+2.5 ReMIX - Lite Launcher")
root.geometry("1280x720")
root.resizable(True, True)

# Original resolution for scaling
original_resolution = (1920, 1080)

# Set minimum and maximum size
root.minsize(480, 270)  # Minimum size (16:9 aspect ratio)
root.maxsize(3840, 2160)  # Maximum size (16:9 aspect ratio)

# Function to load and resize images
def load_image(image_path, size=None):
    img = Image.open(image_path)
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# Images loaded once and dynamically resized later
bg_images = {
    'kh1': Image.open(os.path.join(os.path.dirname(__file__), "kh1.png")),
    'com': Image.open(os.path.join(os.path.dirname(__file__), "com.png")),
    'kh2': Image.open(os.path.join(os.path.dirname(__file__), "kh2.png")),
    'bbs': Image.open(os.path.join(os.path.dirname(__file__), "bbs.png")),
}
game_button_images = {
    'off': Image.open(os.path.join(os.path.dirname(__file__), "game-off.png")),
    'press': Image.open(os.path.join(os.path.dirname(__file__), "game-press.png")),
    'selected': Image.open(os.path.join(os.path.dirname(__file__), "game.png")),
}
play_button_images = {
    'off': Image.open(os.path.join(os.path.dirname(__file__), "play-off.png")),
    'press': Image.open(os.path.join(os.path.dirname(__file__), "play-press.png")),
    'active': Image.open(os.path.join(os.path.dirname(__file__), "play.png")),
}
title_images = {
    'kh1': Image.open(os.path.join(os.path.dirname(__file__), "kh1-title.png")),
    'com': Image.open(os.path.join(os.path.dirname(__file__), "com-title.png")),
    'kh2': Image.open(os.path.join(os.path.dirname(__file__), "kh2-title.png")),
    'bbs': Image.open(os.path.join(os.path.dirname(__file__), "bbs-title.png")),
}

# Positions and sizes
game_button_positions = {
    'kh1': (290, 660),
    'com': (810, 660),
    'kh2': (290, 820),
    'bbs': (810, 820),
}
play_button_position = (1330, 660)

# Canvas with dynamic scaling
canvas = tk.Canvas(root, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)

# State variables
selected_game = None
play_button_active = False
heroic_exe = ""
kh_install_path = ""
json_file_path = ""

# Load configuration from file
def load_config():
    config_file = "launcher_config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
            return config
    return {}

# Save configuration to file
def save_config(config):
    config_file = "launcher_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

#Prompt user to confirm paths to KH_1.5_2.5 installation folder, heroic exe and 68c214c58f694ae88c2dab6f209b43e4.json
def prompt_for_paths():
    config = load_config()

    # Validate Kingdom Hearts Installation Path
    if 'kh_install_path' not in config or not validate_kh_install_path(config.get('kh_install_path')):
        while True:
            kh_install_path = tkinter.filedialog.askdirectory(
                title="Select KH_1.5_2.5 Install Directory")
            if not kh_install_path:
                print("No directory selected, quitting...")
                safe_quit()
                return None, None, None

            if validate_kh_install_path(kh_install_path):
                config['kh_install_path'] = kh_install_path
                break
            else:
                tkinter.messagebox.showerror("Invalid KH_1.5_2.5 Install Directory",
                                        "The selected directory does not appear to contain the necessary Kingdom Hearts game executables.\nPlease select the correct installation folder.")

    # Validate Heroic Executable
    if 'heroic_exe' not in config or not validate_heroic_executable(config.get('heroic_exe')):
        while True:
            heroic_exe = tkinter.filedialog.askopenfilename(
                title="Select Heroic Executable",
                filetypes=[("Executable files", "*.exe")]
            )
            if not heroic_exe:
                print("No Heroic executable selected, quitting...")
                safe_quit()
                return None, None, None

            if validate_heroic_executable(heroic_exe):
                config['heroic_exe'] = heroic_exe
                break
            else:
                tkinter.messagebox.showerror("Invalid Heroic Executable",
                                        "The selected file is not a valid Heroic executable.\nPlease select the correct Heroic.exe file.\nPlease select the correct json file.")

    # Validate 68c214c58f694ae88c2dab6f209b43e4.json Path
    if 'json_file_path' not in config or not validate_json_file(config.get('json_file_path')):
        while True:
            json_file_path = tkinter.filedialog.askopenfilename(
                title="Select 68c214c58f694ae88c2dab6f209b43e4.json",
                filetypes=[("JSON files", "*.json")]
            )
            if not json_file_path:
                print("No JSON file selected, quitting...")
                safe_quit()
                return None, None, None

            if validate_json_file(json_file_path):
                config['json_file_path'] = json_file_path
                break
            else:
                tkinter.messagebox.showerror("Invalid JSON File",
                                        "The selected file is incorrect. Please select the correct 68c214c58f694ae88c2dab6f209b43e4.json file.")

    save_config(config)
    return config['kh_install_path'], config['heroic_exe'], config['json_file_path']

def validate_kh_install_path(path):
    if not path or not os.path.isdir(path):
        return False

    required_games = [
        'KINGDOM HEARTS FINAL MIX.exe',
        'KINGDOM HEARTS Re_Chain of Memories.exe',
        'KINGDOM HEARTS II FINAL MIX.exe',
        'KINGDOM HEARTS Birth by Sleep FINAL MIX FINAL MIX.exe'
    ]
    found_games = 0
    for game in required_games:
        if os.path.exists(os.path.join(path, game)):
            found_games += 1

    # Adjust the threshold as needed.  This example requires at least one game to be present.
    return found_games >= 1

def validate_heroic_executable(exe_path):
    return os.path.exists(exe_path) and os.path.isfile(exe_path) and "heroic" in os.path.basename(exe_path).lower()

def validate_json_file(json_file_path):
    return os.path.exists(json_file_path) and os.path.isfile(json_file_path) and "68c214c58f694ae88c2dab6f209b43e4" in os.path.basename(json_file_path).lower()

# Check for command-line arguments to auto-select a game
def check_launch_arguments():
    if '--kh1' in sys.argv:
        return 'kh1'
    if '--com' in sys.argv:
        return 'com'
    if '--kh2' in sys.argv:
        return 'kh2'
    if '--bbs' in sys.argv:
        return 'bbs'
    return None

def determine_selected_game_from_exe():
    # Load the configuration to get the json_file_path
    config = load_config()
    json_file_path = config.get('json_file_path')

    if not json_file_path or not os.path.exists(json_file_path):
        print(f"Error: JSON file not found or not set in launcher_config.json.")
        return None

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        game_data = data.get("68c214c58f694ae88c2dab6f209b43e4")
        if not game_data:
            print("Error: Game configuration key not found in JSON.")
            return None

        target_exe = game_data.get("targetExe")
        if not target_exe:
            print("Error: `targetExe` is missing or null in the JSON.")
            return None

        exe_name = os.path.basename(target_exe)
        game_exe_map = {
            'KINGDOM HEARTS FINAL MIX.exe': 'kh1',
            'KINGDOM HEARTS Re_Chain of Memories.exe': 'com',
            'KINGDOM HEARTS II FINAL MIX.exe': 'kh2',
            'KINGDOM HEARTS Birth by Sleep FINAL MIX.exe': 'bbs'
        }

        return game_exe_map.get(exe_name)

    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")
        return None

# Example of how to use the path in the update_target_exe function
def update_game_exe(selected_game, game_exe):
    # Load the configuration to get the json_file_path
    config = load_config()
    json_file_path = config.get('json_file_path')

    if not json_file_path:
        print(f"Error: JSON file not found or not set in launcher_config.json.")
        return False

    try:
        # Load the JSON data
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Update the `targetExe` field
        if "68c214c58f694ae88c2dab6f209b43e4" in data:
            data["68c214c58f694ae88c2dab6f209b43e4"]["targetExe"] = game_exe
        else:
            print("Error: Key for the game configuration not found.")
            return False

        # Save the updated JSON
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Successfully updated the `targetExe` field at {json_file_path}.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Launch the selected game via Heroic
def launch_game():
    global heroic_exe, selected_game
    if not heroic_exe or not selected_game:
        print("Heroic executable or selected game not set!")
        return
    subprocess.Popen([heroic_exe, "--no-gui", "--no-sandbox", f"heroic://launch/legendary/68c214c58f694ae88c2dab6f209b43e4"])
    safe_quit()

# Modify the call to prompt_for_paths and handle the additional return value
kh_install_path, heroic_exe, json_file_path = prompt_for_paths()

# Command-line argument check for launching a game directly
selected_game = check_launch_arguments()

if selected_game:
    print(f"Argument detected, auto-selecting and launching {selected_game}.")
    # Update JSON with selected game's executable
    game_exe_map = {
        'kh1': 'KINGDOM HEARTS FINAL MIX.exe',
        'com': 'KINGDOM HEARTS Re_Chain of Memories.exe',
        'kh2': 'KINGDOM HEARTS II FINAL MIX.exe',
        'bbs': 'KINGDOM HEARTS Birth by Sleep FINAL MIX.exe'
    }
    game_exe = os.path.join(kh_install_path, game_exe_map[selected_game])
    update_game_exe(selected_game, game_exe)
    
    # Launch Heroic
    launch_game()
    safe_quit()  # Exit after launching to prevent the UI from loading

#Check json for selected game
selected_game = determine_selected_game_from_exe()

if selected_game:
    print(f"Selected game from the JSON: {selected_game}")
else:
    print("No game detected or an error occurred.")

# Dictionary to hold current ImageTk references
current_images = {}

# Resize event delay (in ms)
resize_delay = 500  # You can adjust this to find the best balance

# Throttle function to handle resizing events with delay
def throttle_resize():
    global resize_event_time
    if resize_event_time is None:
        resize_event_time = root.after(resize_delay, scale_and_redraw)

resize_event_time = None

# Function to scale and redraw all elements
def scale_and_redraw():
    global current_images, resize_event_time
    if resize_event_time is not None:
        root.after_cancel(resize_event_time)
        resize_event_time = None  # Reset the event time

    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()

    # Prevent zero width/height
    if canvas_width <= 0 or canvas_height <= 0:
        return
    
    # Calculate scaling factor
    scale_x = canvas_width / original_resolution[0]
    scale_y = canvas_height / original_resolution[1]
    scale = min(scale_x, scale_y)  # Maintain the largest scale without exceeding the aspect ratio

    # Maintain 16:9 aspect ratio and center the canvas
    new_width = int(original_resolution[0] * scale)
    new_height = int(original_resolution[1] * scale)
    x_offset = (canvas_width - new_width) // 2
    y_offset = (canvas_height - new_height) // 2
    
    # Prevent zero size during scaling
    if new_width <= 0 or new_height <= 0:
        return
    
    canvas.delete("all")  # Clear the canvas for redrawing
    
    # Update background image
    selected_background = bg_images[selected_game or 'kh1']
    resized_bg = selected_background.resize((new_width, new_height), Image.Resampling.LANCZOS)
    current_images['bg'] = ImageTk.PhotoImage(resized_bg)
    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=current_images['bg'], tags="background")
    
    # Update game buttons
    for game, pos in game_button_positions.items():
        x = int(pos[0] * scale) + x_offset
        y = int(pos[1] * scale) + y_offset
        
        # Use appropriate game button image based on selected state
        if selected_game == game:
            resized_button = game_button_images['selected'].resize((int(500 * scale), int(140 * scale)), Image.Resampling.LANCZOS)
        else:
            resized_button = game_button_images['off'].resize((int(500 * scale), int(140 * scale)), Image.Resampling.LANCZOS)
        
        current_images[f'game_{game}'] = ImageTk.PhotoImage(resized_button)
        canvas.create_image(x, y, anchor=tk.NW, image=current_images[f'game_{game}'], tags=f'game_{game}')
        
        resized_title = title_images[game].resize((int(500 * scale), int(140 * scale)), Image.Resampling.LANCZOS)
        current_images[f'title_{game}'] = ImageTk.PhotoImage(resized_title)
        canvas.create_image(x, y, anchor=tk.NW, image=current_images[f'title_{game}'], tags=f'title_{game}')

        # Rebind game button actions after redrawing
        canvas.tag_bind(f'title_{game}', '<ButtonPress-1>', lambda event, g=game: on_game_button_press(event, g, scale))
        canvas.tag_bind(f'title_{game}', '<ButtonRelease-1>', lambda event, g=game: on_game_button_release(event, g))

    # Update play button
    x = int(play_button_position[0] * scale) + x_offset
    y = int(play_button_position[1] * scale) + y_offset
    if selected_game:
        resized_play = play_button_images['active'].resize((int(300 * scale), int(300 * scale)), Image.Resampling.LANCZOS)
    else:
        resized_play = play_button_images['off'].resize((int(300 * scale), int(300 * scale)), Image.Resampling.LANCZOS)
    
    current_images['play'] = ImageTk.PhotoImage(resized_play)
    canvas.create_image(x, y, anchor=tk.NW, image=current_images['play'], tags="play")
    canvas.tag_bind("play", '<Button-1>', lambda event: on_play_button_click(event, scale))
    canvas.tag_bind("play", '<ButtonRelease-1>', lambda event: on_play_button_release(event, scale))

# Throttle the resize event to avoid excessive updates
def on_resize(event):
    throttle_resize()
  
# Game button press and release handlers
def on_game_button_press(event, game, scale):
    if selected_game != game:
        print(f"Pressed {game}")
        # Update the button image to game-press.png, resized to the appropriate scale
        resized_press = game_button_images['press'].resize((int(500 * scale), int(140 * scale)), Image.Resampling.LANCZOS)
        current_images[f'game_{game}_press'] = ImageTk.PhotoImage(resized_press)
        canvas.itemconfig(f'game_{game}', image=current_images[f'game_{game}_press'])

def on_game_button_release(event, game):
    global selected_game, play_button_active
    if selected_game != game:
        selected_game = game
        print(f"Selected {game} - Background Updated")

        # Update the JSON with the selected game's executable
        game_exe_map = {
            'kh1': 'KINGDOM HEARTS FINAL MIX.exe',
            'com': 'KINGDOM HEARTS Re_Chain of Memories.exe',
            'kh2': 'KINGDOM HEARTS II FINAL MIX.exe',
            'bbs': 'KINGDOM HEARTS Birth by Sleep FINAL MIX.exe'
        }
        if kh_install_path:
            game_exe_path = os.path.join(kh_install_path, game_exe_map[selected_game])
            game_exe_path = game_exe_path.replace("\\", "/")  # Replace backslashes with forward slashes
            print(f"Updating {selected_game} executable to {game_exe_path}")
            update_game_exe(selected_game, game_exe_path)
        else:
            print("Error: Kingdom Hearts installation path not set!")

        scale_and_redraw()
        
        play_sound("select.wav")

# Play button click and release handlers
def on_play_button_click(event, scale):
    print("Play button clicked!")
    if selected_game:
        resized_press = play_button_images['press'].resize((int(300 * scale), int(300 * scale)), Image.Resampling.LANCZOS)
        current_images['play_press'] = ImageTk.PhotoImage(resized_press)
        canvas.itemconfig("play", image=current_images['play_press'])
    else:
        print("Play button clicked but no game selected.")
        play_sound("denied.wav")

def on_play_button_release(event, scale):
    print("Play button released!")
    if selected_game:
        resized_active = play_button_images['active'].resize((int(300 * scale), int(300 * scale)), Image.Resampling.LANCZOS)
        current_images['play_active'] = ImageTk.PhotoImage(resized_active)
        canvas.itemconfig("play", image=current_images['play_active'])

        play_sound("confirm.wav")

        launch_game()

# Bind resizing event to redraw with throttling
root.bind("<Configure>", on_resize)

# Main program
if __name__ == "__main__":
    scale_and_redraw()
    root.mainloop()
