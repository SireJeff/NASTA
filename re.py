import telebot
from telebot import types
import pandas as pd
from telebot.types import InputMediaPhoto, InputFile
import threading
import schedule
import time
import datetime
import requests

# Initialize the Telegram Bot with your API token
bot = telebot.TeleBot('6715565004:AAHV7PIs63ARmF_tOFvupO0tkvt7ZkUUgps')

# Group IDs
allowed_group_id = -1001788579325  # Replace with your group ID
reminder_group_id = -1001788579325  # Replace with your reminder group ID

# Load data from the Excel file
excel_file_path = 'ELYAS 5.xlsx'  # Replace with your file path
df = pd.read_excel(excel_file_path)

received_users_file_path = 'received_users.txt'

# Load received user IDs from the file
received_user_ids = set()
try:
    with open(received_users_file_path, 'r') as file:
        for line in file:
            received_user_ids.add(int(line.strip()))
except FileNotFoundError:
    pass

# Events and URL for reminders
events = {
    "2024-06-11 13:30": "زبان عمومی",
    "2024-06-13 09:00": "ریاضی ۲",
    "2024-06-16 09:00": "فیزیک ۳",
    "2024-06-18 09:00": "ریاضی ۱",
    "2024-06-20 15:30": "دیفرانسیل",
    "2024-06-20 09:00": "فیزیک ۲"
    # Add more dates and events as needed
}
url = "https://api.keybit.ir/hadis"

def is_user_in_group(user_id, group_id):
    try:
        member = bot.get_chat_member(group_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking user membership: {e}")
        return False

def send_credentials(user_id):
    global df, received_user_ids

    row = df[df['taken'] == False].iloc[0]
    username = row['USER Names']
    password = row['password']
    hostname = row['hostname']
    port = 38742
    udg = 37300

    message_text = f"""
    {"```نپستر-نت```"}\nRemark: {username}\nSSH Host: `{hostname}` \nUsername: `{username}` \nPassword: `{password}` \nPort: `{port}`\nudgpw port: `{udg}`\n
    {"```NetMod-اندروید/ویندوز```"}\n`ssh://{username}:{password}@{hostname}:{port}/#{username}`\n
    {"```V2box-آیفون```"}\n`ssh://{username}:{password}@{hostname}:{port}#{username}`\n"""

    bot.send_message(user_id, message_text, parse_mode='MarkdownV2')

    ios_images = [
        "ios/i1.jpg",
        "ios/i2.jpg",
        "ios/i3.jpg",
        "ios/i4.jpg",
        "ios/5i.jpg"
    ]
    ios_caption = f"""نحوه اتصال با استفاده از کلاینت NapsternetV در ایفون:\n
    ابتدا برنامه را از اپ استور نصب کرده سپس طبق راهنما کانفیگ داده شده را اضافه کنید.\n
    نکته: جهت اضافه کردن کانفیگ به حروف بزرگ و کوچک دقت کنید.\n
    اگر در اتصال دچار مشکل شدید و یا سرعت کاهش پیدا کرد اقدام به قطع و وصل کردن فیلترشکن کنید\n
    لینک دانلود برنامه از اپ استور (https://apps.apple.com/us/app/napsternetv/id1629465476)"""

    ios_media = []
    for index, image_path in enumerate(ios_images):
        try:
            file = open(image_path, 'rb')
            photo = InputFile(file)
            if index == 0:
                ios_media.append(InputMediaPhoto(media=photo, caption=ios_caption))
            else:
                ios_media.append(InputMediaPhoto(media=photo))
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            continue

    bot.send_media_group(chat_id=user_id, media=ios_media)

    for media_item in ios_media:
        media_item.media.file.close()

    android_images = [
        "android/a1.jpg",
        "android/a2.jpg",
        "android/a3.jpg",
        "android/a4.jpg",
        "android/a5.jpg",
        "android/a6.jpg",
        "android/a7.jpg"
    ]
    android_caption = f"""نحوه اتصال با استفاده از کلاینت NapsternetV در اندروید:\n
    ابتدا برنامه napsternetV را نصب کنید
    سپس طبق راهنما کانفیگ را اضافه کنید.\n
    نکته: جهت اضافه کردن کانفیگ به حروف بزرگ و کوچک دقت کنید.\n
    اگر در اتصال دچار مشکل شدید و یا سرعت کاهش پیدا کرد اقدام به قطع و وصل کردن فیلترشکن کنید\n
    دانلود از گوگل پلی (https://play.google.com/store/apps/details?id=com.napsternetlabs.napsternetv&hl=de&pli=1)\n
    لینک دانلود مستقیم (https://admin.erfan27.me/admin/NapsternetV_62.0.0.apk)"""

    android_media = []
    for index, image_path in enumerate(android_images):
        try:
            file = open(image_path, 'rb')
            photo = InputFile(file)
            if index == 0:
                android_media.append(InputMediaPhoto(media=photo, caption=android_caption))
            else:
                android_media.append(InputMediaPhoto(media=photo))
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            continue

    bot.send_media_group(chat_id=user_id, media=android_media)

    for media_item in android_media:
        media_item.media.file.close()

    received_user_ids.add(user_id)
    df.at[row.name, 'taken'] = True
    df.to_excel(excel_file_path, index=False)

    with open(received_users_file_path, 'a') as file:
        file.write(str(user_id) + '\n')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    print(f"Chat ID: {allowed_group_id}\nUser ID: {user_id}")

    if is_user_in_group(user_id, allowed_group_id):
        if user_id not in received_user_ids:
            send_credentials(user_id)
        else:
            bot.send_message(user_id, "You've already received the message.")
    else:
        bot.send_message(user_id, "You are not a member of the allowed group.")

def send_reminder():
    current_datetime = datetime.datetime.now()
    messagee = "\nزمان برگذاری امتحانات پایانترم\n\n"
    for datetime_str, event in events.items():
        event_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        if event_datetime >= current_datetime:
            time_until_event = event_datetime - current_datetime
            messagee += f"{event} : {time_until_event.days} روز و {time_until_event.seconds // 3600} ساعت دیگر| راس {event_datetime.strftime('%H:%M')} |در تاریخ {event_datetime.strftime('%Y-%m-%d')}\n\n"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        messagee += "\nپا بزن شریف ام‌آی‌تی ایرانه\n\n گنجینه معرفت:\n"
        messagee += data['result']['text']
        messagee += "\n"
        messagee += data['result']['person']
    
    bot.send_message(reminder_group_id, messagee)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the reminder to be sent every 6 hours
schedule.every(6).hours.do(send_reminder)

# Start the scheduling logic in a separate thread
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()

# Run the bot polling in the main thread
bot.polling(none_stop=True)
