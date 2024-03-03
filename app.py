import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import json
import hmac
import hashlib

# Set your Telegram Bot Token
BOT_TOKEN = "7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI"
# Set your NOWPayments API Key and IPN Secret Key
NOWPAYMENTS_API_KEY = "D37DNS7-VH1MPNS-QGM99PV-SQZQG2A"
IPN_SECRET_KEY = "o+HRhmRdFXo8OtZRIldMX0jjUDp90zKx"

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Flask app for handling webhooks
app = Flask(__name__)

# Define a handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the NOWPayments Bot! Send /pay to initiate a payment.")

# Define a handler for the /pay command
def pay(update: Update, context: CallbackContext) -> None:
    # Generate payment link using NOWPayments API
    payment_link = generate_payment_link()
    update.message.reply_text(f"Click the link to complete the payment: {payment_link}")

# Generate a payment link using NOWPayments API
def generate_payment_link() -> str:
    # Specify payment details
    payment_details = {
        "price_amount": 1,
        "price_currency": "usd",
        "pay_currency": "trx",
        "order_id": None,
        "order_description": None,
        "ipn_callback_url": "https://biamoozim.pythonanywhere.com/nowpayments-webhook",
    }

    # Generate NOWPayments API endpoint for creating payment
    create_payment_url = "https://api.nowpayments.io/v1/payment"

    # Send a POST request to create a payment
    response = requests.post(create_payment_url, json=payment_details, headers={"x-api-key": NOWPAYMENTS_API_KEY})
    payment_data = response.json()

    # Return the payment link
    return payment_data.get("payment_url", "Error generating payment link")

# Define a handler for the NOWPayments webhook
@app.route("/nowpayments-webhook", methods=["POST"])
def nowpayments_webhook():
    data = request.get_json()
    if verify_nowpayments_signature(data):
        # Check payment status and handle accordingly
        payment_status = data.get("payment_status")
        if payment_status == "finished":
            user_id = data.get("purchase_id")  # Adjust as needed
            send_congratulations(user_id)
        else:
            send_payment_failure(user_id)
    return "OK"

# Verify NOWPayments webhook signature
def verify_nowpayments_signature(data: dict) -> bool:
    received_signature = request.headers.get("x-nowpayments-sig")
    sorted_data = json.dumps(data, separators=(",", ":"), sort_keys=True)
    calculated_signature = hmac.new(IPN_SECRET_KEY.encode(), sorted_data.encode(), hashlib.sha512).hexdigest()
    return received_signature == calculated_signature

# Notify the user about successful payment
def send_congratulations(user_id: str) -> None:
    # You can use the Telegram API to send a message to the user
    pass

# Notify the user about payment failure
def send_payment_failure(user_id: str) -> None:
    # You can use the Telegram API to send a message to the user
    pass

if __name__ == "__main__":
    # Set up the Telegram bot
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pay", pay))

    # Start the webhook on a dedicated server or localhost
    updater.start_webhook(listen="Biamoozim.pythonanywhere.com", port=8443, url_path=BOT_TOKEN)
    updater.bot.setWebhook(url="https://Biamoozim.pythonanywhere.com/" + BOT_TOKEN)

    # Run the Flask app for handling NOWPayments webhook
    app.run()
