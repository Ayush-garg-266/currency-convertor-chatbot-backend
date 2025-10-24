import streamlit as st
from flask import Flask, request, jsonify
from threading import Thread

# --- Flask app for Dialogflow ---
flask_app = Flask(__name__)


@flask_app.route('/')
def index():
    return "✅ Flask backend is running!"


@flask_app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    print("Dialogflow Request:", data)

    # Example response
    response = {
        "fulfillmentText": "Hello from Streamlit + Flask!"
    }
    return jsonify(response)


def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)


# --- Streamlit interface ---
st.set_page_config(page_title="Dialogflow + Streamlit Webhook")

st.title("🌐 Dialogflow Webhook Server")
st.write("This app runs a Flask backend to receive Dialogflow requests.")
st.write("Webhook URL:")
st.code("https://your-app-name.streamlit.app/webhook", language="text")

# Start Flask in background
Thread(target=run_flask).start()
