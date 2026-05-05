from tools import system, browser

from agent.memory import memory

import re
 
class Executor:

    """Executes parsed action steps"""

    def __init__(self):

        self.action_map = {

            "open_start":   system.open_start_menu,

            "press_enter":  system.press_enter,

            "wait":         lambda: system.wait(2),

            "open_browser": lambda: browser.open_browser(),

            "click_search": browser.click_search_bar,

            "draw_circle":  system.draw_circle,

        }

    def execute(self, steps):

        """

        Execute all steps in the plan

        Args:

            steps: List of action strings

        Returns:

            Success status

        """

        print("\n" + "="*60)

        print("🚀 EXECUTING PLAN")

        print("="*60 + "\n")

        succeeded = 0

        failed    = 0

        for i, step in enumerate(steps, 1):

            print(f"\n[Step {i}/{len(steps)}] {step}")

            try:

                success = self.execute_single_step(step)

                if success:

                    memory.add(step, "success")

                    succeeded += 1

                else:

                    memory.add(step, "failed", "Unknown action")

                    failed += 1

            except Exception as e:

                print(f"  ❌ Error: {e}")

                memory.add(step, "failed", str(e))

                failed += 1

        print("\n" + "="*60)

        print("✅ EXECUTION COMPLETE")

        print("="*60 + "\n")

        summary = memory.get_summary()

        print(f"📊 Summary: {summary['successes']} succeeded, {summary['failures']} failed")

        return True

    def execute_single_step(self, step):

        """Execute a single action step"""

        step_lower = step.lower().strip()

        # ── DIRECT ACTION MAPPING ─────────────────────────────

        if step_lower in self.action_map:

            print(f"  ▶ Executing: {step_lower}")

            self.action_map[step_lower]()

            return True

        # ── NAVIGATION & APP CONTROL ──────────────────────────
 
        # open_app APP_NAME

        if step_lower.startswith("open_app "):

            app = step_lower.replace("open_app ", "", 1).strip()

            print(f"  ▶ Opening app: {app}")

            system.open_app(app)

            return True

        # close_app APP_NAME

        if step_lower.startswith("close_app "):

            app = step_lower.replace("close_app ", "", 1).strip()

            print(f"  ▶ Closing app: {app}")

            system.close_app(app)

            return True

        # switch_app APP_NAME

        if step_lower.startswith("switch_app "):

            app = step_lower.replace("switch_app ", "", 1).strip()

            print(f"  ▶ Switching to app: {app}")

            system.switch_app(app)

            return True

        # close_window

        if step_lower == "close_window":

            print("  ▶ Closing current window...")

            system.close_window()

            return True

        # switch_window

        if step_lower == "switch_window":

            print("  ▶ Switching window...")

            system.switch_window()

            return True

        # wait_for_window TITLE

        if step_lower.startswith("wait_for_window_close "):

            title = step_lower.replace("wait_for_window_close ", "", 1).strip()

            print(f"  ▶ Waiting for window to close: {title}")

            system.wait_for_window_close(title)

            return True

        if step_lower.startswith("wait_for_window "):

            title = step_lower.replace("wait_for_window ", "", 1).strip()

            print(f"  ▶ Waiting for window: {title}")

            system.wait_for_window(title)

            return True

        # ── KEYBOARD ACTIONS ──────────────────────────────────
 
        # type TEXT

        if step_lower.startswith("type "):

            text = step.replace("type ", "", 1).strip()

            print(f"  ▶ Typing: {text}")

            system.type_text(text)

            return True

        # press KEY

        if step_lower.startswith("press "):

            key = step_lower.replace("press ", "", 1).strip()

            print(f"  ▶ Pressing key: {key}")

            system.press_key(key)

            return True

        # hotkey CTRL+S

        if step_lower.startswith("hotkey "):

            keys = step_lower.replace("hotkey ", "", 1).strip()

            print(f"  ▶ Pressing hotkey: {keys}")

            system.hotkey(keys)

            return True

        # ── MOUSE ACTIONS ─────────────────────────────────────
 
        # click X Y

        if step_lower.startswith("click "):

            coords = re.findall(r'\d+', step_lower)

            if len(coords) >= 2:

                x, y = int(coords[0]), int(coords[1])

                print(f"  ▶ Clicking at: ({x}, {y})")

                system.click(x, y)

                return True

        # move_mouse X Y

        if step_lower.startswith("move_mouse "):

            coords = re.findall(r'\d+', step_lower)

            if len(coords) >= 2:

                x, y = int(coords[0]), int(coords[1])

                print(f"  ▶ Moving mouse to: ({x}, {y})")

                system.move_mouse(x, y)

                return True

        # scroll_down

        if step_lower == "scroll_down":

            print("  ▶ Scrolling down...")

            system.scroll_down()

            return True

        # scroll_up

        if step_lower == "scroll_up":

            print("  ▶ Scrolling up...")

            system.scroll_up()

            return True

        # ── WAIT & TIMING ─────────────────────────────────────
 
        # wait or wait X

        if step_lower.startswith("wait"):

            duration = re.findall(r'\d+', step_lower)

            if duration:

                print(f"  ▶ Waiting {duration[0]} seconds...")

                system.wait(int(duration[0]))

            else:

                print("  ▶ Waiting 2 seconds...")

                system.wait(2)

            return True

        # wait_for_image IMAGE_NAME

        if step_lower.startswith("wait_for_image "):

            image = step_lower.replace("wait_for_image ", "", 1).strip()

            print(f"  ▶ Waiting for image: {image}")

            system.wait_for_image(image)

            return True

        # wait_for_text TEXT

        if step_lower.startswith("wait_for_text "):

            text = step_lower.replace("wait_for_text ", "", 1).strip()

            print(f"  ▶ Waiting for text: {text}")

            system.wait_for_text(text)

            return True

        # wait_for_condition CONDITION

        if step_lower.startswith("wait_for_condition "):

            condition = step_lower.replace("wait_for_condition ", "", 1).strip()

            print(f"  ▶ Waiting for condition: {condition}")

            system.wait_for_condition(condition)

            return True

        # ── WEB & BROWSER ACTIONS ─────────────────────────────
 
        # search_web TEXT

        if step_lower.startswith("search_web "):

            query = step_lower.replace("search_web ", "", 1).strip()

            print(f"  ▶ Searching web: {query}")

            browser.search_web(query)

            return True

        # click_video

        if step_lower == "click_video":

            print("  ▶ Clicking video...")

            browser.click_video()

            return True

        # ── MS PAINT TOOL SELECTION ───────────────────────────
 
        # select_pencil

        if step_lower == "select_pencil":

            print("  ▶ Selecting Pencil tool...")

            system.select_paint_tool("Pencil")

            return True

        # select_brush

        if step_lower == "select_brush":

            print("  ▶ Selecting Brush tool...")

            system.select_paint_tool("Brush")

            return True

        # select_erase

        if step_lower == "select_erase":

            print("  ▶ Selecting Eraser tool...")

            system.select_paint_tool("Eraser")

            return True

        # select_fill

        if step_lower == "select_fill":

            print("  ▶ Selecting Fill tool...")

            system.select_paint_tool("Fill")

            return True

        # select_text

        if step_lower == "select_text":

            print("  ▶ Selecting Text tool...")

            system.select_paint_tool("Text")

            return True

        # select_line

        if step_lower == "select_line":

            print("  ▶ Selecting Line tool...")

            system.select_paint_tool("Line")

            return True

        # select_rectangle

        if step_lower == "select_rectangle":

            print("  ▶ Selecting Rectangle tool...")

            system.select_paint_tool("Rectangle")

            return True

        # select_ellipse

        if step_lower == "select_ellipse":

            print("  ▶ Selecting Ellipse tool...")

            system.select_paint_tool("Ellipse")

            return True

        # select_circle

        if step_lower == "select_circle":

            print("  ▶ Selecting Circle tool...")

            system.select_paint_tool("Circle")

            return True

        # ── MS PAINT SETTINGS ─────────────────────────────────
 
        # select_color COLOR_NAME

        if step_lower.startswith("select_color "):

            color = step_lower.replace("select_color ", "", 1).strip()

            print(f"  ▶ Selecting color: {color}")

            system.select_paint_color(color)

            return True

        # select_size SIZE

        if step_lower.startswith("select_size "):

            size = step_lower.replace("select_size ", "", 1).strip()

            print(f"  ▶ Selecting size: {size}")

            system.select_paint_size(size)

            return True

        # ── MS PAINT DRAWING ──────────────────────────────────
 
        # draw_circle

        if step_lower == "draw_circle":

            print("  ▶ Drawing circle...")

            system.draw_circle()

            return True

        # draw_rectangle

        if step_lower == "draw_rectangle":

            print("  ▶ Drawing rectangle...")

            system.draw_rectangle()

            return True

        # draw_line

        if step_lower == "draw_line":

            print("  ▶ Drawing line...")

            system.draw_line()

            return True

        # ── SCREEN READING & ANALYSIS ─────────────────────────
 
        # screenshot

        if step_lower == "screenshot":

            print("  ▶ Taking screenshot...")

            system.screenshot()

            return True

        # read_screen

        if step_lower == "read_screen":

            print("  ▶ Reading screen...")

            result = system.read_screen()

            print(f"  📄 Screen text: {result}")

            return True

        # analyze_screen

        if step_lower == "analyze_screen":

            print("  ▶ Analyzing screen...")

            result = system.analyze_screen()

            print(f"  🔍 Screen analysis: {result}")

            return True

        # ── CLIPBOARD ACTIONS ─────────────────────────────────
 
        # set_clipboard TEXT

        if step_lower.startswith("set_clipboard "):

            text = step.replace("set_clipboard ", "", 1).strip()

            print(f"  ▶ Setting clipboard: {text}")

            system.set_clipboard(text)

            return True

        # get_clipboard

        if step_lower == "get_clipboard":

            print("  ▶ Getting clipboard...")

            result = system.get_clipboard()

            print(f"  📋 Clipboard: {result}")

            return True

        # ── SYSTEM & PROCESS ──────────────────────────────────
 
        # check_file_exists FILE_PATH

        if step_lower.startswith("check_file_exists "):

            path = step.replace("check_file_exists ", "", 1).strip()

            print(f"  ▶ Checking file: {path}")

            result = system.check_file_exists(path)

            print(f"  📁 File exists: {result}")

            return True

        # check_process_exists PROCESS

        if step_lower.startswith("check_process_exists "):

            process = step_lower.replace("check_process_exists ", "", 1).strip()

            print(f"  ▶ Checking process: {process}")

            result = system.check_process_exists(process)

            print(f"  ⚙️ Process running: {result}")

            return True

        # execute_script SCRIPT_NAME

        if step_lower.startswith("execute_script "):

            script = step_lower.replace("execute_script ", "", 1).strip()

            print(f"  ▶ Executing script: {script}")

            system.execute_script(script)

            return True

        # play_sound SOUND_NAME

        if step_lower.startswith("play_sound "):

            sound = step_lower.replace("play_sound ", "", 1).strip()

            print(f"  ▶ Playing sound: {sound}")

            system.play_sound(sound)

            return True

        # log MESSAGE

        if step_lower.startswith("log "):

            message = step.replace("log ", "", 1).strip()

            print(f"  📝 Log: {message}")

            return True

        # ── CONTROL FLOW ──────────────────────────────────────
 
        # repeat N ACTIONS

        if step_lower.startswith("repeat "):

            parts = step_lower.split()

            if len(parts) >= 2 and parts[1].isdigit():

                n = int(parts[1])

                print(f"  ▶ Repeat {n} times noted")

            return True

        # end_repeat

        if step_lower == "end_repeat":

            print("  ▶ End repeat")

            return True

        # if_condition CONDITION

        if step_lower.startswith("if_condition "):

            condition = step_lower.replace("if_condition ", "", 1).strip()

            print(f"  ▶ If condition: {condition}")

            return True

        # else_condition

        if step_lower == "else_condition":

            print("  ▶ Else condition")

            return True

        # end_condition

        if step_lower == "end_condition":

            print("  ▶ End condition")

            return True

        # end_if

        if step_lower == "end_if":

            print("  ▶ End if")

            return True

        # end_else

        if step_lower == "end_else":

            print("  ▶ End else")

            return True

        # repeat_until_condition CONDITION

        if step_lower.startswith("repeat_until_condition "):

            condition = step_lower.replace(

                "repeat_until_condition ", "", 1

            ).strip()

            print(f"  ▶ Repeat until: {condition}")

            return True

        # ── CUSTOM ACTIONS ────────────────────────────────────
 
        # custom_action PARAMS

        if step_lower.startswith("custom_action "):

            params = step_lower.replace("custom_action ", "", 1).strip()

            print(f"  ▶ Custom action: {params}")

            system.custom_action(params)

            return True

        # custom_condition PARAMS

        if step_lower.startswith("custom_condition "):

            params = step_lower.replace("custom_condition ", "", 1).strip()

            print(f"  ▶ Custom condition: {params}")

            system.custom_condition(params)

            return True

        # ── UNKNOWN ACTION ────────────────────────────────────

        print(f"  ⚠️ Unknown action: {step_lower}")

        return False
 
 
def execute(steps):

    """Convenience function to execute steps"""

    executor = Executor()

    return executor.execute(steps)
 