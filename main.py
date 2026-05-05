#!/usr/bin/env python3
"""
Computer Use Agent - Main Entry Point

This agent can perform computer tasks based on natural language commands.
"""

import os
import sys
from agent.planner import create_plan
from agent.parser import clean_and_parse
from agent.executor import execute
from agent.memory import memory
from llm.ollama import check_ollama_status
from vision.screen import capture_screen

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🤖 COMPUTER USE AGENT")
    print("="*60)
    print("Automate your computer with natural language commands!")
    print("="*60 + "\n")

def check_prerequisites():
    """Check if all requirements are met"""
    print("🔍 Checking prerequisites...\n")
    
    # Check Ollama
    status, message = check_ollama_status()
    print(f"  Ollama: {'✅' if status else '❌'} {message}")
    
    if not status:
        print("\n⚠️ Please start Ollama:")
        print("   1. Install: https://ollama.ai")
        print("   2. Run: ollama run llama3.2")
        return False
    
    # Check PyAutoGUI
    try:
        import pyautogui
        print(f"  PyAutoGUI: ✅ Installed")
    except ImportError:
        print(f"  PyAutoGUI: ❌ Not installed")
        print("\n⚠️ Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All prerequisites met!\n")
    return True

def main():
    """Main execution loop"""
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    # Create screenshots directory
    os.makedirs("screenshots", exist_ok=True)
    
    # Main loop
    while True:
        try:
            # Get user goal
            goal = input("🎯 Enter your goal (or 'quit' to exit): ").strip()
            
            if goal.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not goal:
                continue
            
            # Optional: Capture screen for context
            # screenshot_path = capture_screen()
            
            # Step 1: Create plan
            print("\n🧠 Planning...")
            plan = create_plan(goal)
            
            if not plan:
                print("❌ Failed to create plan. Check Ollama connection.")
                continue
            
            # Step 2: Parse plan
            print("\n📋 Parsing plan...")
            try:
                steps = clean_and_parse(plan)
                print(f"✅ Parsed {len(steps)} steps:")
                for i, step in enumerate(steps, 1):
                    print(f"   {i}. {step}")
            except Exception as e:
                print(f"❌ Failed to parse plan: {e}")
                continue
            
            # Step 3: Confirm execution
            confirm = input("\n⚠️  Execute these steps? (yes/no): ").strip().lower()
            
            if confirm not in ['yes', 'y']:
                print("⏭️  Skipped execution\n")
                continue
            
            # Step 4: Execute
            execute(steps)
            
            # Show memory
            print("\n📚 Recent actions:")
            for action in memory.get_recent(5):
                status_icon = "✅" if action["status"] == "success" else "❌"
                print(f"  {status_icon} {action['action']}")
            
            print("\n" + "-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue

if __name__ == "__main__":
    main()