import requests
import json
from config import OLLAMA_MODEL, OLLAMA_URL

def generate(prompt, temperature=0.3):
    """
    Generate response from Ollama LLM
    
    Args:
        prompt: The prompt to send to the model
        temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
    
    Returns:
        The generated text response
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "options": {
                "num_predict": 500
            }
        }, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            print(f"Error: Ollama returned status code {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return None
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

def check_ollama_status():
    """Check if Ollama is running and the model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if OLLAMA_MODEL in model_names or f"{OLLAMA_MODEL}:latest" in model_names:
                return True, f"Ollama is running with model: {OLLAMA_MODEL}"
            else:
                return False, f"Model {OLLAMA_MODEL} not found. Available: {model_names}"
        return False, "Ollama not responding"
    except:
        return False, "Ollama is not running"