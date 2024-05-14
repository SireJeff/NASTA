import schedule
import time
import datetime
import telebot
import requests
# Initialize the Telegram Bot with your API token
bot = telebot.TeleBot('6715565004:AAHV7PIs63ARmF_tOFvupO0tkvt7ZkUUgps')


url = "https://api.keybit.ir/hadis"

response = requests.get(url)
group_id = -1001788579325


# Define your specific dates and events
events = {
    "2024-06-11 13:30": "زبان عمومی",
    "2024-06-13 09:00": "ریاضی ۲",
    "2024-06-16 09:00": "فیزیک ۳",
    "2024-06-18 09:00": "ریاضی ۱",
    "2024-06-20 15:30": "دیفرانسیل",
    "2024-06-20 09:00": "فیزیک ۲"
    # Add more dates and events as needed
}

def send_reminder():
    current_datetime = datetime.datetime.now()
    messagee="\nزمان برگذاری امتحانات پایانترم\n\n"
    for datetime_str, event in events.items():
        event_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        if event_datetime >= current_datetime:
            time_until_event = event_datetime - current_datetime
            messagee +=f"{event} : {time_until_event.days} روز و {time_until_event.seconds // 3600} ساعت دیگر| راس {event_datetime.strftime('%H:%M')} |در تاریخ {event_datetime.strftime('%Y-%m-%d')}\n\n"
    if response.status_code == 200:
        data = response.json()
        messagee+="\nپا بزن شریف ام‌آی‌تی ایرانه\n\n گنجینه معرفت:\n"
        messagee+=data['result']['text']
        messagee+="\n"
        messagee+=data['result']['person']

    bot.send_message(group_id , messagee)  # Replace with your Telegram group ID

send_reminder()

# Schedule the reminder to be sent every 6 hours
schedule.every(6).hours.do(send_reminder)  # Adjust the time according to your timezone

# Function to start the bot polling in a separate thread
def bot_polling():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
            time.sleep(10)  # Sleep for a while before polling again in case of exceptions

# Start the bot polling in a separate thread
bot_thread = threading.Thread(target=bot_polling)
bot_thread.start()

# Main loop to run schedule
while True:
    schedule.run_pending()
    time.sleep(1)