from flask import Flask, render_template, request, Response
import time
import waitress
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    def generate_response():
        if user_message:
            # EXAMPLE
            response = "Team formation: <Alez 1>, <Alez 2>, <Alez 3>, <Alez 4>, <Alez 5>. \nThis is a response from the bot. Processing more data... Here's some additional information... Final response complete."

            # Extract player names from the team message using regex
            # player_names = re.findall(r'<(.*?)>', response)  # Find all names inside '<>'
            # player_list = [name.strip() for name in player_names]  # Clean names

            for char in response:
                yield f"{char}"
                time.sleep(0.01)  # Simulate typing effect
        else:
            fallback_message = "I didn't catch that. Could you please repeat?"
            for char in fallback_message:
                yield f"{char}"
                time.sleep(0.01)  # Simulate typing effect for fallback message

    return Response(generate_response(), mimetype='text/event-stream')

# python -m waitress --host=0.0.0.0 --port=5001 project.app:app
if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=5001)
