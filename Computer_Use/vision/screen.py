import pyautogui
import os
from config import SCREENSHOT_PATH

def capture_screen(save_path=None):
    """
    Capture screenshot of entire screen
    
    Args:
        save_path: Where to save screenshot (uses config default if None)
    
    Returns:
        Path to saved screenshot
    """
    if save_path is None:
        save_path = SCREENSHOT_PATH
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    
    print(f"📸 Screenshot saved: {save_path}")
    return save_path

def get_screen_size():
    """Get screen dimensions"""
    return pyautogui.size()

def capture_region(x, y, width, height, save_path="region.png"):
    """Capture specific region of screen"""
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(save_path)
    return save_path