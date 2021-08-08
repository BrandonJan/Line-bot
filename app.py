# webapp

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'xakdF6ruYdjbFraP0ObFhoWbXB3atErk9Zj/mmw/PTHohmjQldc2JtH40J7UKV40Xup6to0p6YHjV6B3SqqBtsG5n2haqaKLpsnNJLmtXNMgSSwQabAY6bDqYTkDRrIpkiRDcQF0eL3Pedq743ffHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18e7d0225c2c1bb4d8caab3468a84f03')

# 來接收伺服器端傳來的訊息，收到後再執行此function


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

# 回覆使用者傳來的訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '抱歉，我聽不懂您再說什麼'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='24')
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return

    if msg in ['hi', 'Hi']:  # 如果訊息中包含Hi或hi
        r == '嗨'

    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '您想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))#原本的程式是回直接回覆重複你說的話


# 在直接被執行main finction而不適被載入而已的話才開始跑程式
if __name__ == "__main__":
    app.run()
