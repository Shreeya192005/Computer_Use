from llm.ollama import generate
import json

def create_plan(goal, context=""):
    prompt = f"""You are a computer automation assistant. Your job is to create step-by-step instructions to accomplish user goals on a Windows computer.
 
IMPORTANT RULES:

1. Return ONLY a Python list of strings

2. Each step should be a simple, clear action

3. Use EXACT action keywords from the list below

4. NO explanations, NO markdown, NO code blocks

5. Just the list

6. Always add "wait" after opening any application

7. Always select a tool BEFORE drawing in Paint

8. Always select a color BEFORE drawing in Paint
 
AVAILABLE ACTIONS:
 
--- NAVIGATION & APP CONTROL ---

- "open_start"                        - Opens Windows Start Menu (Win key)

- "open_app APP_NAME"                 - Opens a specific application (e.g., open_app notepad)

- "close_app APP_NAME"                - Closes a specific application

- "switch_app APP_NAME"               - Switches to a specific application

- "close_window"                      - Closes current window (Alt+F4)

- "switch_window"                     - Switches to next window (Alt+Tab)

- "wait_for_window WINDOW_TITLE"      - Waits until a window with specified title appears

- "wait_for_window_close TITLE"       - Waits until a window with specified title closes
 
--- KEYBOARD ACTIONS ---

- "type TEXT"                         - Types the specified text

- "press_enter"                       - Presses Enter key

- "hotkey CTRL+S"                     - Save file

- "hotkey CTRL+C"                     - Copy

- "hotkey CTRL+V"                     - Paste

- "hotkey CTRL+Z"                     - Undo

- "hotkey CTRL+A"                     - Select all

- "hotkey ALT+F4"                     - Close window

- "hotkey WIN+D"                      - Show desktop
 
--- MOUSE ACTIONS ---

- "click X Y"                         - Left click at screen coordinates (e.g., click 500 300)

- "move_mouse X Y"                    - Move mouse to coordinates (e.g., move_mouse 400 200)

- "scroll_down"                       - Scrolls page down

- "scroll_up"                         - Scrolls page up
 
--- WAIT & TIMING ---

- "wait"                              - Wait 2 seconds

- "wait_for_image IMAGE_NAME"         - Waits until a specific image appears on screen

- "wait_for_text TEXT"                - Waits until specific text appears on screen

- "wait_for_condition CONDITION"      - Waits until a custom condition is met
 
--- WEB & BROWSER ACTIONS ---

- "open_browser"                      - Opens default web browser

- "click_search"                      - Clicks on browser search bar

- "search_web TEXT"                   - Searches for TEXT on the web

- "click_video"                       - Clicks on video element (for YouTube)
 
--- MS PAINT TOOL SELECTION ---

  IMPORTANT: Always select tool first, then select color, then draw

- "select_Pencil"                     - Selects Pencil tool in Paint

- "select_Brush"                      - Selects Brush tool in Paint

- "select_Erase"                      - Selects Eraser tool in Paint

- "select_Fill"                       - Selects Fill/Bucket tool in Paint

- "select_Text"                       - Selects Text tool in Paint

- "select_Line"                       - Selects Line tool in Paint

- "select_Rectangle"                  - Selects Rectangle tool in Paint

- "select_Ellipse"                    - Selects Ellipse tool in Paint

- "select_Circle"                     - Selects Circle tool in Paint
 
--- MS PAINT SETTINGS ---

- "select_Color COLOR_NAME"           - Selects a color (e.g., select_Color red, select_Color blue)

- "select_Size SIZE"                  - Selects brush size 1-5 (e.g., select_Size 3)
 
--- MS PAINT DRAWING ---

  IMPORTANT: Tool and color MUST be selected before drawing

- "draw_circle"                       - Draws a circle using mouse in Paint

- "draw_rectangle"                    - Draws a rectangle using mouse in Paint

- "draw_line"                         - Draws a line using mouse in Paint
 
--- SCREEN READING & ANALYSIS ---

- "screenshot"                        - Takes a screenshot and saves to disk

- "read_screen"                       - Uses OCR to read text from screen

- "analyze_screen"                    - Analyzes screen content and returns description
 
--- CLIPBOARD ACTIONS ---

- "set_clipboard TEXT"                - Sets the clipboard to specified text

- "get_clipboard"                     - Gets the current clipboard content
 
--- SYSTEM & PROCESS ---

- "check_file_exists FILE_PATH"       - Checks if a file exists at specified path

- "check_process_exists PROCESS_NAME" - Checks if a process is running

- "execute_script SCRIPT_NAME"        - Executes a predefined script

- "play_sound SOUND_NAME"             - Plays a specific sound

- "Log MESSAGE"                       - Logs a message to the console
 
--- CONTROL FLOW ---

- "repeat N ACTIONS"                  - Repeats a set of actions N times

- "end_repeat"                        - Ends a repeat block

- "if_condition CONDITION"            - Executes actions if condition is met

- "else_condition"                    - Executes if previous condition not met

- "end_condition"                     - Ends an if/else block

- "end_if"                            - Ends an if block

- "end_else"                          - Ends an else block

- "repeat_until_condition CONDITION"  - Repeats actions until condition is met
 
--- CUSTOM ACTIONS ---

- "custom_action PARAMS"              - Executes a custom action with parameters

- "custom_condition PARAMS"           - Evaluates a custom condition with parameters
 
EXAMPLES:
 
Goal: "open notepad and type hello"

Response:

["open_start", "type notepad", "press_enter", "wait", "type hello"]
 
Goal: "search for cats on youtube"

Response:

["open_browser", "wait", "click_search", "type youtube.com", "press_enter", "wait", "click_search", "type cats", "press_enter"]
 
Goal: "open ms paint and draw a circle"

Response:

["open_start", "type paint", "press_enter", "wait", "wait", "select_Circle", "select_Color black", "select_Size 2", "draw_circle"]
 
Goal: "open ms paint and draw a red rectangle"

Response:

["open_start", "type paint", "press_enter", "wait", "wait", "select_Rectangle", "select_Color red", "select_Size 2", "draw_rectangle"]
 
Goal: "open ms paint draw a blue line"

Response:

["open_start", "type paint", "press_enter", "wait", "wait", "select_Line", "select_Color blue", "select_Size 2", "draw_line"]
 
Goal: "open ms paint write text hello"

Response:

["open_start", "type paint", "press_enter", "wait", "wait", "select_Text", "select_Color black", "click 400 300", "type Hello"]
 
Goal: "open ms paint and fill background red"

Response:

["open_start", "type paint", "press_enter", "wait", "wait", "select_Fill", "select_Color red", "click 400 300"]
 
Goal: "take a screenshot and save"

Response:

["screenshot", "hotkey CTRL+S"]
 
Goal: "open notepad type hello and save"

Response:

["open_start", "type notepad", "press_enter", "wait", "type Hello World", "hotkey CTRL+S"]
 
Goal: "search google for python tutorials"

Response:

["open_browser", "wait", "click_search", "type google.com", "press_enter", "wait", "click_search", "type python tutorials", "press_enter"]
 
Now create a plan for this goal:
 
Goal: {goal}
 
Response (ONLY the Python list, no explanations, no markdown):"""
 

    response = generate(prompt, temperature=0.1)
    
    if response:
        print(f"\n🧠 LLM Response:\n{response}\n")
        return response
    else:
        return None

def create_visual_plan(goal, screen_description):
    """
    Create plan based on visual screen analysis (advanced)
    """
    prompt = f"""Based on what's visible on screen, create a plan.

Screen: {screen_description}
Goal: {goal}

Return a Python list of actions."""

    return generate(prompt, temperature=0.2)