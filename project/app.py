from flask import Flask, render_template, request, Response
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    
    def generate_response():
        if user_message:
            responses = "This is a response from the bot. Processing more data... Here's some additional information... Final response complete."
            
            for char in responses:
                yield f"{char}"
                time.sleep(0.01)  # Adding a small delay to simulate typing effect
        else:
            fallback_message = "I didn't catch that. Could you please repeat?"
            for char in fallback_message:
                yield f"{char}"
                time.sleep(0.01)  # Simulate typing effect for fallback message

    return Response(generate_response(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
