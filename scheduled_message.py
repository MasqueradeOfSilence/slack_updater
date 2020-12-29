import schedule
import time
import yagmail
import os
from datetime import date
from slack.web.client import WebClient
from slack.errors import SlackApiError

# Must adhere to naming conventions: lanternX
def get_file_number():
    count_file = open("count.txt", "r")
    number = count_file.read(1)
    count_file.close()
    number = int(number)
    print("number: ", number)
    new_number = number + 1
    count_file = open("count.txt", "w")
    count_file.write(str(new_number))
    count_file.close()
    return number

def post_file(slack_client):
    print("Posting video...")
    number = get_file_number()
    try:
        video_file = open("/Users/Alex/Documents/alex_video" + str(number) + ".mov", "rb")
    except:
        print("Error opening the video file!")
    try:
        slack_client.files_upload(
        channels="C01HHDPSFP0",
        initial_comment="Hey all, <@alexcn711> submitted an FX iteration!",
        file=video_file)
    except SlackApiError as e:
        print("ERROR, request to Slack API Failed: ", e)
    video_file.close()

def remind_me():
    print("Sending reminder...")
    username = "summerdragon322"
    # Using yagmail keychain
    yag = yagmail.SMTP(username)
    to = "alexcn711@gmail.com"
    subject = "Reminder! " + str(date.today())
    text = "Alex, your updated video will be posted in 1 hour. Don't forget to post it with correct naming: lanternX."
    yag.send(to, subject, text)

if __name__ == "__main__":
    print("Starting app...")
    # For a test workspace currently
    SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
    slack_client = WebClient(SLACK_BOT_TOKEN)

    remind_me()
    post_file(slack_client)

    schedule.every().sunday.at("19:00").do(lambda: remind_me())
    schedule.every().sunday.at("20:00").do(lambda: post_file(slack_client))
    schedule.every().tuesday.at("19:00").do(lambda: remind_me())
    schedule.every().tuesday.at("20:00").do(lambda: post_file(slack_client))

    while True:
        schedule.run_pending()
        time.sleep(5)
