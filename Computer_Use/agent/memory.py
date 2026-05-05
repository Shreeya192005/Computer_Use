from datetime import datetime

class Memory:
    """Simple memory system to track agent actions and outcomes"""
    
    def __init__(self):
        self.history = []
        self.successes = []
        self.failures = []
    
    def add(self, action, status="executed", details=""):
        """Add an action to memory"""
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "status": status,
            "details": details
        }
        self.history.append(entry)
        
        if status == "success":
            self.successes.append(entry)
        elif status == "failed":
            self.failures.append(entry)
    
    def get_recent(self, n=5):
        """Get n most recent actions"""
        return self.history[-n:] if self.history else []
    
    def get_all(self):
        """Get all history"""
        return self.history
    
    def get_summary(self):
        """Get execution summary"""
        return {
            "total_actions": len(self.history),
            "successes": len(self.successes),
            "failures": len(self.failures)
        }
    
    def clear(self):
        """Clear all memory"""
        self.history.clear()
        self.successes.clear()
        self.failures.clear()

# Global memory instance
memory = Memory()