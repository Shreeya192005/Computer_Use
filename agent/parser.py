import ast
import re

def clean_and_parse(plan_text):
    """
    Parse the LLM's plan into a structured list of steps
    
    Args:
        plan_text: Raw text from LLM
    
    Returns:
        List of action steps
    """
    if not plan_text:
        raise ValueError("Empty plan received")
    
    # Remove markdown code blocks if present
    plan_text = re.sub(r'```python\s*', '', plan_text)
    plan_text = re.sub(r'```\s*', '', plan_text)
    
    # Remove any leading/trailing whitespace
    plan_text = plan_text.strip()
    
    # Try to find a list pattern
    list_pattern = r'\[.*?\]'
    match = re.search(list_pattern, plan_text, re.DOTALL)
    
    if match:
        plan_text = match.group(0)
    
    try:
        # Parse as Python literal
        steps = ast.literal_eval(plan_text)
        
        if not isinstance(steps, list):
            raise ValueError("Parsed result is not a list")
        
        # Clean up steps
        cleaned_steps = []
        for step in steps:
            if isinstance(step, str):
                cleaned_steps.append(step.strip())
        
        return cleaned_steps
        
    except (SyntaxError, ValueError) as e:
        print(f"❌ Parsing failed. Raw output:\n{plan_text}\n")
        
        # Fallback: try to extract steps manually
        lines = plan_text.split('\n')
        steps = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                # Remove quotes and common list markers
                line = re.sub(r'^[\d\.\-\*\)]+\s*', '', line)
                line = line.strip('"\'')
                if line:
                    steps.append(line)
        
        if steps:
            print("⚠️ Used fallback parser")
            return steps
        
        raise Exception(f"Failed to parse plan: {e}")

def validate_steps(steps):
    """Validate that steps contain known actions"""
    valid_actions = [
        "open_start", "type", "press_enter", "wait", 
        "click_search", "search_web", "open_browser",
        "draw_circle", "click", "move_mouse"
    ]
    
    for step in steps:
        action = step.split()[0] if step else ""
        if action not in valid_actions and not any(va in step for va in valid_actions):
            print(f"⚠️ Unknown action in step: {step}")
    
    return True