import pyautogui

import time
 
# ── MS PAINT FUNCTIONS ────────────────────────────────────
 
def select_paint_tool(tool_name):

    """Selects a tool in MS Paint"""

    tool_positions = {

        "Pencil":    (156, 57),

        "Brush":     (190, 57),

        "Eraser":    (224, 57),

        "Fill":      (122, 57),

        "Text":      (258, 57),

        "Line":      (156, 85),

        "Rectangle": (190, 85),

        "Ellipse":   (224, 85),

        "Circle":    (224, 85),

    }

    if tool_name in tool_positions:

        x, y = tool_positions[tool_name]

        pyautogui.click(x, y)

        time.sleep(0.5)

        print(f"  ✅ Tool selected: {tool_name}")

    else:

        print(f"  ⚠️ Unknown tool: {tool_name}")
 
def select_paint_color(color_name):

    """Selects a color in MS Paint palette"""

    color_positions = {

        "black":  (403, 57),

        "white":  (420, 57),

        "red":    (437, 57),

        "orange": (454, 57),

        "yellow": (471, 57),

        "green":  (488, 57),

        "blue":   (505, 57),

        "purple": (522, 57),

        "pink":   (539, 57),

        "brown":  (556, 57),

        "gray":   (573, 57),

    }

    color = color_name.lower()

    if color in color_positions:

        x, y = color_positions[color]

        pyautogui.click(x, y)

        time.sleep(0.5)

        print(f"  ✅ Color selected: {color_name}")

    else:

        print(f"  ⚠️ Unknown color: {color_name}")
 
def select_paint_size(size):

    """Selects brush size in MS Paint"""

    size_positions = {

        "1": (290, 57),

        "2": (290, 65),

        "3": (290, 73),

        "4": (290, 81),

        "5": (290, 89),

    }

    size_str = str(size)

    if size_str in size_positions:

        x, y = size_positions[size_str]

        pyautogui.click(x, y)

        time.sleep(0.5)

        print(f"  ✅ Size selected: {size}")

    else:

        print(f"  ⚠️ Unknown size: {size}")
 
def draw_circle():

    """Draws a circle on MS Paint canvas"""

    import pygetwindow as gw

    import time

    # Step 1: Find and focus MS Paint window

    windows = gw.getWindowsWithTitle("Paint")

    if not windows:

        print("  ⚠️ MS Paint window not found!")

        return

    paint_window = windows[0]

    paint_window.activate()  # Bring Paint to front

    time.sleep(1)  # Wait for focus to settle

    # Step 2: Select Ellipse/Circle tool first

    select_paint_tool("Ellipse")

    time.sleep(0.5)

    # Step 3: Click on canvas area first to ensure focus

    pyautogui.click(500, 350)  # Click inside canvas

    time.sleep(0.3)

    # Step 4: Now draw the circle

    pyautogui.moveTo(400, 250)

    time.sleep(0.3)

    pyautogui.mouseDown()

    time.sleep(0.2)

    pyautogui.moveTo(600, 450, duration=1.0)

    time.sleep(0.2)

    pyautogui.mouseUp()

    time.sleep(0.5)

    print("  ✅ Circle drawn")
  
def draw_rectangle(): 

    """Draws a rectangle on MS Paint canvas"""

    pyautogui.moveTo(300, 200)

    time.sleep(0.3)

    pyautogui.mouseDown()

    time.sleep(0.2)

    pyautogui.moveTo(600, 400, duration=1.0)

    time.sleep(0.2)

    pyautogui.mouseUp()

    time.sleep(0.5)

    print("  ✅ Rectangle drawn")
 
def draw_line():

    """Draws a line on MS Paint canvas"""

    pyautogui.moveTo(200, 300)

    time.sleep(0.3)

    pyautogui.mouseDown()

    time.sleep(0.2)

    pyautogui.moveTo(700, 300, duration=1.0)

    time.sleep(0.2)

    pyautogui.mouseUp()

    time.sleep(0.5)

    print("  ✅ Line drawn")
 
# ── OTHER SYSTEM FUNCTIONS ────────────────────────────────
 
def open_app(app_name):

    import subprocess

    subprocess.Popen(app_name)

    time.sleep(1)
 
def close_app(app_name):

    import subprocess

    subprocess.run(f"taskkill /f /im {app_name}.exe", shell=True)
 
def switch_app(app_name):

    import pyautogui

    pyautogui.hotkey("alt", "tab")

    time.sleep(0.5)
 
def close_window():

    pyautogui.hotkey("alt", "f4")

    time.sleep(0.5)
 
def switch_window():

    pyautogui.hotkey("alt", "tab")

    time.sleep(0.5)
 
def hotkey(keys):

    key_list = keys.lower().split("+")

    pyautogui.hotkey(*key_list)

    time.sleep(0.3)
 
def move_mouse(x, y):

    pyautogui.moveTo(x, y, duration=0.5)
 
def scroll_down():

    pyautogui.scroll(-3)

    time.sleep(0.3)
 
def scroll_up():

    pyautogui.scroll(3)

    time.sleep(0.3)
 
def screenshot():

    import datetime

    filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    pyautogui.screenshot(filename)

    print(f"  ✅ Screenshot saved: {filename}")
 
def set_clipboard(text):

    import pyperclip

    pyperclip.copy(text)
 
def get_clipboard():

    import pyperclip

    return pyperclip.paste()
 
def check_file_exists(path):

    import os

    return os.path.exists(path)
 
def check_process_exists(process_name):

    import subprocess

    result = subprocess.run(

        f"tasklist /fi \"imagename eq {process_name}\"",

        capture_output=True, text=True, shell=True

    )

    return process_name.lower() in result.stdout.lower()
 
def wait_for_window(title):

    import pygetwindow as gw

    while True:

        windows = gw.getWindowsWithTitle(title)

        if windows:

            break

        time.sleep(0.5)
 
def wait_for_window_close(title):

    import pygetwindow as gw

    while True:

        windows = gw.getWindowsWithTitle(title)

        if not windows:

            break

        time.sleep(0.5)
 
def read_screen():

    import pytesseract

    from PIL import ImageGrab

    screenshot = ImageGrab.grab()

    text = pytesseract.image_to_string(screenshot)

    return text
 
def analyze_screen():

    screenshot()

    return "Screen analyzed"
 
def wait_for_image(image_name):

    while True:

        try:

            location = pyautogui.locateOnScreen(image_name)

            if location:

                break

        except:

            pass

        time.sleep(0.5)
 
def wait_for_text(text):

    while True:

        screen_text = read_screen()

        if text.lower() in screen_text.lower():

            break

        time.sleep(0.5)
 
def custom_action(params):

    print(f"  ▶ Custom action: {params}")
 
def custom_condition(params):

    print(f"  ▶ Custom condition: {params}")
 
def execute_script(script_name):

    print(f"  ▶ Executing script: {script_name}")
 
def play_sound(sound_name):

    import winsound

    winsound.PlaySound(sound_name, winsound.SND_FILENAME)
 
def wait_for_condition(condition):

    print(f"  ▶ Waiting for condition: {condition}")

    time.sleep(1)

def click(x, y):

    pyautogui.click(x, y)

    time.sleep(0.3)

    print(f"  ✅ Clicked at ({x}, {y})")
 
def type_text(text):

    pyautogui.typewrite(text, interval=0.05)

    time.sleep(0.3)

    print(f"  ✅ Typed: {text}")
 
def press_key(key):

    pyautogui.press(key)

    time.sleep(0.3)

    print(f"  ✅ Pressed key: {key}")
 
def press_enter():

    pyautogui.press("enter")

    time.sleep(0.3)

    print("  ✅ Pressed Enter")
 
def wait(seconds):

    time.sleep(seconds)

    print(f"  ✅ Waited {seconds}s")
 
def open_start_menu():

    pyautogui.press("win")

    time.sleep(1)

    print("  ✅ Opened Start Menu")
 
 