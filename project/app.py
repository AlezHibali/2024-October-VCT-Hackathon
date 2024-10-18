from flask import Flask, render_template, request, Response
import time
import waitress
import re
import random

CURRENT_FUN_FACT_INDEX = 0


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


@app.route('/api/funfact', methods=['GET'])
def fun_fact():
    # HARDCODED FUN FACTS
    fun_facts = [
        "Fun Fact 1: Honey never spoils.",
        "Fun Fact 2: Bananas are berries, but strawberries aren't.",
        "Fun Fact 3: Octopuses have three hearts.",
    ]
    # Select a random fun fact diff from last one
    global CURRENT_FUN_FACT_INDEX
    new_index = CURRENT_FUN_FACT_INDEX
    while new_index == CURRENT_FUN_FACT_INDEX:
        new_index = random.randint(0, len(fun_facts) - 1)
    CURRENT_FUN_FACT_INDEX = new_index
    fact = fun_facts[new_index]

    return {"fun_fact": fact}


# python -m waitress --host=0.0.0.0 --port=5001 project.app:app
if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=5001)
