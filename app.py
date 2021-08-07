# webapp

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'xakdF6ruYdjbFraP0ObFhoWbXB3atErk9Zj/mmw/PTHohmjQldc2JtH40J7UKV40Xup6to0p6YHjV6B3SqqBtsG5n2haqaKLpsnNJLmtXNMgSSwQabAY6bDqYTkDRrIpkiRDcQF0eL3Pedq743ffHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18e7d0225c2c1bb4d8caab3468a84f03')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
