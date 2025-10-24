import streamlit as st
from flask import Flask, request, jsonify
from threading import Thread
import requests

# ---------- Flask App ----------
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Currency Converter Webhook is running!"

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)

    # Dialogflow parameters
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = round(amount * cf, 2)

    response = {
        'fulfillmentText': f"{amount} {source_currency} is {final_amount} {target_currency}"
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = f"https://free.currconv.com/api/v7/convert?q={source}_{target}&compact=ultra&apiKey=c829b3c7d4fc848239bd6da8"
    res = requests.get(url).json()
    return res[f'{source}_{target}']

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Currency Converter Webhook")
st.title("💰 Currency Converter Chatbot Backend")
st.write("This app runs Flask to handle Dialogflow webhook requests.")
st.write("Webhook URL:")
st.code("https://your-app-name.streamlit.app/webhook", language="text")

# Start Flask in a background thread
Thread(target=run_flask).start()
