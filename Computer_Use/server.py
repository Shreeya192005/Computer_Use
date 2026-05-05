"""
Optional web server for the Computer Use Agent
Run with: python server.py
"""

from flask import Flask, request, jsonify, render_template_string
from agent.planner import create_plan
from agent.parser import clean_and_parse
from agent.executor import execute
import threading

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Computer Use Agent</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        input { width: 100%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; margin-top: 10px; }
        #result { margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🤖 Computer Use Agent</h1>
    <input type="text" id="goal" placeholder="Enter your goal (e.g., open notepad)">
    <button onclick="executeGoal()">Execute</button>
    <div id="result"></div>
    
    <script>
        function executeGoal() {
            const goal = document.getElementById('goal').value;
            document.getElementById('result').innerHTML = 'Executing...';
            
            fetch('/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({goal: goal})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('result').innerHTML = 
                    '<h3>Plan:</h3><pre>' + JSON.stringify(data.steps, null, 2) + '</pre>' +
                    '<h3>Status:</h3>' + data.status;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/execute', methods=['POST'])
def execute_goal():
    data = request.json
    goal = data.get('goal', '')
    
    # Create plan
    plan = create_plan(goal)
    steps = clean_and_parse(plan)
    
    # Execute in background
    threading.Thread(target=execute, args=(steps,)).start()
    
    return jsonify({
        'status': 'executing',
        'steps': steps
    })

if __name__ == '__main__':
    print("🌐 Server running on http://localhost:5000")
    app.run(debug=True, port=5000)