import webbrowser
import time
import pyautogui
from config import DELAY_MEDIUM, DELAY_LONG

def open_browser(url=""):
    """Open default browser"""
    print(f"  ▶ Opening browser{f' with URL: {url}' if url else ''}...")
    if url:
        webbrowser.open(url)
    else:
        webbrowser.open("https://www.google.com")
    time.sleep(DELAY_LONG)

def search_web(query):
    """Search on Google"""
    print(f"  ▶ Searching web for: {query}")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    time.sleep(DELAY_LONG)

def open_youtube():
    """Open YouTube"""
    print("  ▶ Opening YouTube...")
    webbrowser.open("https://www.youtube.com")
    time.sleep(DELAY_LONG)

def click_search_bar():
    """Click on browser search bar (approximate location)"""
    print("  ▶ Clicking search bar...")
    screen_width, screen_height = pyautogui.size()
    # Search bar is usually near top center
    search_x = screen_width // 2
    search_y = 100
    pyautogui.click(search_x, search_y)
    time.sleep(DELAY_MEDIUM)

def click_video():

    """Clicks on a video element on screen (e.g. YouTube player or browser video)"""

    import pyautogui

    import time

    try:

        # Try to find and click a video element on screen using image recognition

        location = pyautogui.locateCenterOnScreen("video_player.png", confidence=0.7)

        if location:

            pyautogui.click(location)

            print("  ✅ Clicked video (image match)")

    except Exception:

        # Fallback: click center of screen (common for fullscreen videos)

        screen_width, screen_height = pyautogui.size()

        pyautogui.click(screen_width // 2, screen_height // 2)

        print("  ✅ Clicked video (center of screen)")

    time.sleep(0.5)
 