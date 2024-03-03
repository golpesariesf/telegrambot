from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import uuid

TOKEN = "7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI"
NOWPAYMENT_API_KEY = "D37DNS7-VH1MPNS-QGM99PV-SQZQG2A"
NOWPAYMENT_TID = "2eb7650e-03a0-4202-a3de-f59269ba83d6"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "سلام! برای شروع پرداخت، لطفاً از لینک زیر استفاده کنید:\n"
        "https://sandbox.nowpayments.io/payment/?iid=5752251420"
    )

def check_payment_status(update: Update, context: CallbackContext) -> None:
    payment_code = context.args[0]
    response = requests.get(
        f"https://api.nowpayments.io/v1/payment/{payment_code}",
        headers={"x-api-key": NOWPAYMENT_API_KEY}
    )
    payment_status = response.json().get("payment_status")
    
    if payment_status == "COMPLETED":
        unique_id = uuid.uuid4()
        unique_id_str = unique_id.hex
        update.message.reply_text(f"پرداخت با موفقیت انجام شد!\nکد یکتا: {unique_id_str}")
    else:
        update.message.reply_text("پرداخت هنوز کامل نشده است. لطفاً بعداً مجدداً تلاش کنید.")

def start_bot() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check_payment", check_payment_status, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    start_bot()
