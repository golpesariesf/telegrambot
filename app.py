import telebot
from telebot import types
import pynowpayments

# اطلاعات ربات
bot_token = "7137673728:AAE85wL1RBYskkrlCZaIzhEbgKmiEBiefDI"
bot_id = 5986365049

# اطلاعات Nowpayments
api_key = "D37DNS7-VH1MPNS-QGM99PV-SQZQG2A"
tid = "2eb7650e-03a0-4202-a3de-f59269ba83d6"

# Nowpayments client
nowpayments = pynowpayments.Nowpayments(api_key, tid)

# ربات تلگرام
bot = telebot.TeleBot(bot_token)

# تابعی برای ایجاد لینک پرداخت
def create_payment_link(amount, currency):
    return nowpayments.create_payment(amount, currency)

# تابعی برای بررسی وضعیت پرداخت
def check_payment_status(payment_id):
    return nowpayments.get_payment_details(payment_id)

# هندلر شروع ربات
@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "سلام! برای دریافت لینک پرداخت، لطفا مبلغ و واحد پول را به صورت زیر وارد کنید:\n\nمبلغ واحد پول\n\nمثال:\n\n10000 IRR")

# هندلر دریافت اطلاعات پرداخت
@bot.message_handler(func=lambda message: message.text.split())
def payment_info_handler(message):
    try:
        amount, currency = message.text.split()
        amount = float(amount)
        
        # ایجاد لینک پرداخت
        payment_link = create_payment_link(amount, currency)

        # ارسال لینک پرداخت به کاربر
        bot.send_message(message.chat.id, f"لینک پرداخت:\n\n{payment_link}")
    except Exception as e:
        bot.send_message(message.chat.id, "اطلاعات وارد شده صحیح نیست. لطفا مجددا تلاش کنید.")

# هندلر پیگیری وضعیت پرداخت
@bot.message_handler(commands=["check"])
def check_payment_handler(message):
    try:
        payment_id = message.text.split()[1]
        
        # بررسی وضعیت پرداخت
        payment_status = check_payment_status(payment_id)

        # ارسال نتیجه به کاربر
        if payment_status["status"] == "paid":
            bot.send_message(message.chat.id, "پرداخت با موفقیت انجام شد.")
        else:
            bot.send_message(message.chat.id, "پرداخت هنوز انجام نشده است.")
    except Exception as e:
        bot.send_message(message.chat.id, "شناسه تراکنش صحیح نیست. لطفا مجددا تلاش کنید.")

# ربات را اجرا کنید
bot.polling()
