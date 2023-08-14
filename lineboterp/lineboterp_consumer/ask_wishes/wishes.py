from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from product.buy_now import *
from product.product_preorder import *
import lineboterp
from database import single_imagetolink,wishessend

def wishes():
    id = lineboterp.user_id
    state = lineboterp.user_state
    message = lineboterp.msg
    message_storage = lineboterp.storage
    #商品名稱,商品圖片,推薦原因,願望建立時間,會員_LINE_ID,資料來源
    #使用者行為過濾
    userfilter = ['重新填寫','取消','營業資訊','團購商品','【預購商品】列表','【現購商品】列表','訂單/購物車查詢',
                    '訂單查詢','未取訂單列表','預購訂單列表','歷史訂單列表','【訂單詳細】','【加入購物車】',
                    '查看購物車','【修改數量】','修改購物車清單','【清單移除商品】','取消修改清單',
                    '【送出購物車訂單】','問題提問','許願商品','【立即購買】','【手刀預購】',
                    '【現購列表下一頁】','【預購列表下一頁】','資料庫','測試','圖片']
    if message not in userfilter:
        if state[id] == 'wishes':
            message_storage[id+'wishesname'] = message #商品名稱
            if len(message) <= 15:
                message_storage[id+'wishesall'] = f"1.許願商品名稱：{message}"
                edit_text = f"{message_storage[id+'wishesall']}\n=>2.請打字輸入推薦原因：(100字內)"
                message_storage[id+'wishesstep'] += 1
                check_text = fill_out_the_screen(edit_text,message_storage[id+'wishesstep'])
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishesreason'
            else:
                check_text = TextSendMessage(text = f"1.許願商品名稱：「{message}」，長度大於15個字請縮短文字呦～")
        elif state[id] == 'wishesreason':
            message_storage[id+'wishesreason'] = message #推薦原因
            if len(message) <= 100:
                message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n2.推薦原因：{message}"
                edit_text = f"{message_storage[id+'wishesall']}\n=>3.請打字輸入資料來源：(可以是連結呦～)"
                message_storage[id+'wishesstep'] += 1
                check_text = fill_out_the_screen(edit_text,message_storage[id+'wishesstep'])
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishessource'
            else:
                check_text = TextSendMessage(text = f"2.推薦原因：「{message}」，長度大於100個字請縮短文字呦～")
        elif state[id] == 'wishessource':
            message_storage[id+'wishessource'] = message #資料來源
            message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n3.資料來源：{message}"
            edit_text = f"{message_storage[id+'wishesall']}\n=>4.請上傳商品圖片："
            message_storage[id+'wishesstep'] += 1
            check_text = fill_out_the_screen(edit_text,message_storage[id+'wishesstep'])
            message_storage[id+'userfilter'] = check_text
            state[id] = 'wishesimg'
        elif state[id] == 'wishesimg':
            if '.jpg' in message_storage[id+'img']:#檢查暫存的圖片內容路徑
                single_imagetolink()#執行圖片轉換連結(單張)
                message_storage[id+'wishesall'] = f"{message_storage[id+'wishesall']}\n4.圖片產生連結：{message_storage[id+'imagelink']}"
                check_info = {
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": f"{message_storage[id+'imagelink']}",
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "許願商品填寫確認",
                                "weight": "bold",
                                "size": "xl",
                                "align": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "lg",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{message_storage[id+'wishesall']}",
                                        "wrap": True,
                                        "color": "#666666",
                                        "size": "sm",
                                        "flex": 5
                                    }
                                    ]
                                }
                                ]
                            }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                            {
                                "type": "button",
                                "height": "sm",
                                "action": {
                                "type": "message",
                                "label": "願望送出",
                                "text": "願望送出"
                                },
                                "style": "primary",
                                "color": "#B17157"
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                "type": "message",
                                "label": "重新填寫",
                                "text": "重新填寫"
                                }
                            },
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                "type": "message",
                                "label": "取消",
                                "text": "取消"
                                }
                            }
                            ],
                            "flex": 0
                        }
                        }
                check_text =FlexSendMessage(
                            alt_text='願望商品填寫確認',
                            contents={
                                "type": "carousel",
                                "contents": [check_info]   
                                } 
                            )
                message_storage[id+'userfilter'] = check_text
                state[id] = 'wishescheck'
            else:
                check_text = TextSendMessage(text='4.您傳送的不是圖片，請打開聊天室圖片庫發送圖片！')
        elif state[id] == 'wishescheck':
            wishesname = message_storage[id+'wishesname']
            wishesreason = message_storage[id+'wishesreason']
            wishessource = message_storage[id+'wishessource']
            img = message_storage[id+'img']
            confirmationmessage = wishessend(wishesname,wishesreason,wishessource,img)
            if confirmationmessage == 'ok':
                check_text = TextSendMessage(text='許願商品已經成功建立囉～')
            else:
                check_text = TextSendMessage(text='許願商品建立時發生錯誤！請稍後再試～')
            wishesname = 'NaN'
            wishesreason = 'NaN'
            wishessource = 'NaN'
            img = 'NaN'
            state[id] = 'normal'
    else:
        #取消或重新填寫都將所有有關願望商品的暫存取消
        message_storage[id+'wishesname'] = 'NaN'
        message_storage[id+'wishesreason'] = 'NaN'
        message_storage[id+'wishessource'] = 'NaN'
        message_storage[id+'img'] = 'NaN'
        if message == '重新填寫':
            state[id] = 'wishes'
            message_storage[id+'userfilter'] = "NaN"
            message_storage[id+'wishesstep'] = 1
            check_text = initial_fill_screen()
        elif message == '取消':
            state[id] = 'normal'
            check_text = TextSendMessage(text = '您的許願商品填寫流程\n已經取消囉～')
        else:
            cancelmessage = f"您傳送的訊息「{message}」不在許願商品填寫流程中的內容\n如果想取消請點擊下方取消按鈕～"
            if message_storage[id+'userfilter'] == 'NaN':
                check_text = TextSendMessage(text = cancelmessage),initial_fill_screen()
            else:
                check_text = TextSendMessage(text = cancelmessage),message_storage[id+'userfilter']
    return check_text

#填寫畫面1
def initial_fill_screen():
    screen_information = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rGlTAt3.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "許願商品填寫(1/4)",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": "=>1.許願商品名稱(15字內)：請打字輸入",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "取消",
                        "text": "取消"
                        }
                    }
                    ],
                    "flex": 0
                }
                }

    initial_fill_screen_show = FlexSendMessage(
                alt_text='願望商品填寫',
                contents={
                    "type": "carousel",
                    "contents": [screen_information]   
                    } 
                )
    return initial_fill_screen_show
#填寫畫面2～4
def fill_out_the_screen(allcontent,wishesstep):
    screen_information = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.imgur.com/rGlTAt3.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": f"許願商品填寫({wishesstep}/4)",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "text",
                                "text": f"{allcontent}",
                                "wrap": True,
                                "color": "#666666",
                                "size": "sm",
                                "flex": 5
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "重新填寫",
                        "text": "重新填寫"
                        },
                        "color": "#B17157",
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "取消",
                        "text": "取消"
                        }
                    }
                    ],
                    "flex": 0
                }
                }

    fill_out_the_screen_show = FlexSendMessage(
                alt_text='購物車訂單確認',
                contents={
                    "type": "carousel",
                    "contents": [screen_information]   
                    } 
                )
    return fill_out_the_screen_show