import pytesseract
from PIL import Image
from config import OCR_ENABLED, TESSERACT_PATH
import os

# Set Tesseract path
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(image_path):
    """
    Extract text from image using OCR
    
    Args:
        image_path: Path to image file
    
    Returns:
        Extracted text as string
    """
    if not OCR_ENABLED:
        return "OCR disabled"
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def find_text_on_screen(search_text, screenshot_path):
    """
    Find if specific text exists on screen
    
    Returns:
        Boolean indicating if text was found
    """
    screen_text = extract_text(screenshot_path)
    return search_text.lower() in screen_text.lower()

def get_screen_description(screenshot_path):
    """Get a description of what's on screen via OCR"""
    text = extract_text(screenshot_path)
    
    if text:
        # Return first 200 characters as summary
        return text[:200] + "..." if len(text) > 200 else text
    return "No text detected on screen"