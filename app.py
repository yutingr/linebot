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

# Channel Access Token
line_bot_api = LineBotApi('8gJCs4UU2pCyEeWKiGM5H1goheoUCKIz362oIhO3Jr1jZFq4lG/OsRMEKCevFHa32E5FwXWmrNvVf2GowlG5xnCpHK9CzNa+7/d1U1isJkJOsVFCtR1egXyg9dHJOF4teGvK3UfA12VZg/Sokgqx6QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('db4369800ec743d6d3220de2f0b81868')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

def KeyWord(text):
    KeyWordDict = {"你好":"今天天氣如何?",
                   "掰掰":"Bye Bye"}
    for k in KeyWordDict.keys():
        if text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

def Button(event):
    message = TemplateSendMessage(
            alt_text='Buttons template', 
            template=ButtonsTemplate(
                    thumbnail_image_url='https://www.amazon.com/Disney-Stitch-Soft-Touch-Magnet/dp/B00GDI4A68',
                    title='Menu', 
                    text='Please select', 
                    actions=[
                            PostbackTemplateAction(
                                    label='postback',
                                    text='postback text',
                                    data='postback1'
                                    ),
                            MessageTemplateAction(
                                    label='ButtonsTemplate',
                                    text='ButtonsTemplate'
                                    ),
                            URITemplateAction(
                                    label='VIDEO1',
                                    uri='http://example.com/'
                                    )
                            ]
                    )
                )
    line_bot_api.reply_message(event.reply_token, message)

def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = event.message.text))

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        Button(event)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))
#    message = TextSendMessage(text=event.message.text)
#    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
