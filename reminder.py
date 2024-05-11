import schedule
import time
import datetime
import telebot

# Initialize the Telegram Bot with your API token
bot = telebot.TeleBot('6848355878:AAG_zxLVh_klI4FUIMHv0HrsPtULngnMgUA')

# Define your specific dates and events
events = {
    "2024-06-11 13:30": "زبان عمومی",
    "2024-06-13 09:00": "ریاضی ۲",
    "2024-06-16 09:00": "فیزیک ۳",
    "2024-06-18 09:00": "ریاضی ۱",
    "2024-06-20 15:30": "معادلات دیفرانسیل",
    "2024-06-20 09:00": "فیزیک ۲"
    # Add more dates and events as needed
}
@bot.message_handler(commands=['start'], func=lambda message: message.text)
def send_reminder(message):
    current_datetime = datetime.datetime.now()
    messagee="\nزمان برگذاری امتحانات پایانترم\n"
    for datetime_str, event in events.items():
        event_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        if event_datetime >= current_datetime:
            time_until_event = event_datetime - current_datetime
            messagee +=f" پایانترم {event} : {time_until_event.days} روز و {time_until_event.seconds // 3600} ساعت دیگر| راس {event_datetime.strftime('%H:%M')} |در تاریخ {event_datetime.strftime('%Y-%m-%d')}\n"
    bot.send_message(message.chat.id, messagee)  # Replace with your Telegram group ID

# Function to send reminders for upcoming events

# Schedule the reminder to be sent every day at 8:00 AM (GMT+03:30)
schedule.every().day.at("04:00").do(send_reminder)  # Adjust the time according to your timezone

# Main loop to keep the script running
while True:
    bot.polling()
    schedule.run_pending()
    time.sleep(1)
