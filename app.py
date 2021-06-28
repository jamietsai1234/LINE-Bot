import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("uAZ2+TUeav7CdsB2q08XzunFdz8yROekcrXCuUP5kHox+/3Gcw8SOoe4DvWFxHsiefB4/ruMoU2OUvIYqj+8uPvQB3xCqBelePMKWzic7aEluZCxk9GTvew9DsRlcTkM+IcwH3J0WA4Wn9YXhXldnQdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.environ.get("e8aa52cfa588dd63ccbcca7b81960c7d"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
