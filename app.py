# from flask import Flask, render_template, request, jsonify, json
# import requests

# RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/webhook", methods=["POST"])
# def webhook():
#     user_message = request.json["message"]
#     print("User Message:", user_message)

#     # Send user message to Rasa and get chatbot's response
#     rasa_response = requests.post(RASA_API_URL, json={"message": user_message})
#     rasa_response_json = rasa_response.json()

#     print("Rasa Response:", rasa_response_json)

#     bot_response = (
#         rasa_response_json[0]["text"]
#         if rasa_response_json
#         else "Sorry, I did't understand that."
#     )

#     return jsonify({"response": bot_response})


# if __name__ == "__main__":
#     app.run(debug=True, port=3000)

from flask import Flask, render_template, request, jsonify
import requests

ACTION_ENDPOINT = "http://localhost:5055/webhook"
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        user_message = request.json["message"]
        print("User Message:", user_message)

        # Send user message to the custom action server and get chatbot's response
        action_response = requests.post(ACTION_ENDPOINT, json={"message": user_message})
        action_response.raise_for_status()  # Raise an error for bad responses
        action_response_json = action_response.json()

        print("Action Response:", action_response_json)

        if action_response_json and isinstance(action_response_json, list):
            bot_response = action_response_json[0].get(
                "text", "Sorry, I didn't understand that."
            )
        else:
            bot_response = "Sorry, I didn't understand that."

        return jsonify({"response": bot_response})

    except KeyError:
        return jsonify({"response": "Error: 'message' key not found in the request."})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the custom action server: {e}")
        return jsonify(
            {"response": "Sorry, there was an issue processing your request."}
        )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
