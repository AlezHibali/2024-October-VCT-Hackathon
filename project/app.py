from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if user_message:
        # Simulate bot response
        response = {"bot_message": "This is a response from the bot."}
    else:
        response = {"bot_message": "I didn't catch that. Could you please repeat?"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
