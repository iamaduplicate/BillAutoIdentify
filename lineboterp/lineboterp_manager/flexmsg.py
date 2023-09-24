from linebot.models import FlexSendMessage
import mysql.connector
import requests
from datetime import datetime, timedelta
import time
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import imgurinfo
import os, io, pyimgur, glob
import manager



def alls_manufacturers_name_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                    "type": "message",
                    "label": "選擇此廠商",
                    "text": f"庫存-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                }
                ],
                "spacing": "none",
                "margin": "none"
            }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message


def allp_manufacturers_name_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                      "type": "message",
                      "label": "選擇此廠商",
                      "text": f"進貨-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                  }
                ],
                "spacing": "none",
                "margin": "none"
              }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message


#----------------修改-查詢所有廠商名稱--------------------
def allr_manufacturers_name_flex_msg(result):    
    if result is not None:
        bubbles = []
        for row in result:
            mid = row[0]
            mname = row[1]
            bubble = {               
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                  {
                    "type": "text",
                    "text": "廠商查詢",
                    "size": "xl",
                    "weight": "bold"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": f"【廠商編號】: {mid}",
                            "weight": "bold",
                            "margin": "sm",
                            "flex": 0
                          },
                          {
                            "type": "text",
                            "text": f"【廠商名稱】: {mname}",
                            "flex": 0,
                            "margin": "sm",
                            "weight": "bold"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#888888"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "none",
                    "action": {
                      "type": "message",
                      "label": "選擇此廠商",
                      "text": f"修改-選擇廠商 {mid}"
                    },
                    "height": "md",
                    "offsetEnd": "none",
                    "offsetBottom": "sm"
                  }
                ],
                "spacing": "none",
                "margin": "none"
              }
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})
    
    return flex_message

#--------------依廠商->庫存資訊---------------
def stock_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[2]  # '庫存數量'
            sell_price = row[3]  # '售出單價'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"庫存數量: {stock_num}"},
                        {"type": "text", "text": f"售出單價: {sell_price}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message
'''def stock_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[2]  # '庫存數量'
            sell_price = row[3]  # '售出單價'

            bubble = {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "商品信息", "color": "#ffffff", "align": "start", "size": "sm"},
                        {"type": "text", "text": f"商品名稱: {pname}", "color": "#ffffff", "size": "lg", "margin": "md"},
                    ],
                    "backgroundColor": "#0074c2",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}", "size": "sm", "color": "#555555"},
                        {"type": "text", "text": f"庫存數量: {stock_num}", "size": "sm", "color": "#555555"},
                        {"type": "text", "text": f"售出單價: {sell_price}", "size": "sm", "color": "#555555"},
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "button", "style": "primary", "color": "#0074c2", "action": {"type": "message", "label": "查看詳細", "text": f"詳細 {pid}"}},
                        {"type": "button", "style": "secondary", "color": "#dddddd", "action": {"type": "message", "label": "加入購物車", "text": f"加入購物車 {pid}"}},
                    ],
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message'''


#-----------------依分類->庫存資訊-----------------
def stock_categoryate_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            stock_num = row[5]  # '庫存數量'
            sell_price = row[7]  # '售出單價'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        {"type": "text", "text": f"庫存數量：{stock_num}"},
                        {"type": "text", "text": f"售出單價：{sell_price}"},
                    ]
                }
            }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

#--------------依廠商->進貨資訊---------------
def purchase_manufacturers_flex_msg(result):
    if result:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            pname = row[19]  # '商品名稱'
            purch_num = row[13]  # '進貨數量'
            purch_price = row[14]  # '進貨單價'
            purch_time = row[15]  # '進貨時間'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨數量: {purch_num}"},
                        {"type": "text", "text": f"進貨單價: {purch_price}"},
                        {"type": "text", "text": f"進貨時間: {purch_time}"}

                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message

#-----------------依分類->進貨資訊-----------------
def purchase_categoryate_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            pname = row[19]  # '商品名稱'
            purch_num = row[13]  # '進貨數量'
            purch_price = row[14]  # '進貨單價'
            purch_time = row[15]  # '進貨時間'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨數量: {purch_num}"},
                        {"type": "text", "text": f"進貨單價: {purch_price}"},
                        {"type": "text", "text": f"進貨時間: {purch_time}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message


def new_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[1]  # '商品ID'
            mid = row[0]  # '廠商編號'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"廠商編號：{mid}"},
                        
                    ]
                }
            }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

def rev_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        
                    ]
                },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "margin": "none",
                            "action": {
                            "type": "message",
                            "label": "修改此商品進貨資訊",
                            "text": f"修改-商品{pid}"
                            },
                            "height": "md",
                            "offsetEnd": "none",
                            "offsetBottom": "sm"
                        }
                        ],
                        "spacing": "none",
                        "margin": "none"
                    }
                    }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

def revc_pur_info_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'

            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID：{pid}"},
                        {"type": "text", "text": f"商品名稱：{pname}"},
                        
                    ]
                },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#905c44",
                            "margin": "none",
                            "action": {
                            "type": "message",
                            "label": "修改此商品進貨資訊",
                            "text": f"修改-商品{pid}"
                            },
                            "height": "md",
                            "offsetEnd": "none",
                            "offsetBottom": "sm"
                        }
                        ],
                        "spacing": "none",
                        "margin": "none"
                    }
                    }
            bubbles.append(bubble)

        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    else:
        flex_message = FlexSendMessage(
            alt_text="類別下所有商品",
            contents={
                "type": "text",
                "text": "找不到符合條件的資料。"
            }
        )
    return flex_message

'''def puring_pro_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            purstate = row[2]  # '進貨狀態'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨狀態: {purstate}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此商品進貨中列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品進貨中列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message'''

def puring_pro_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            purstate = row[2]  # '進貨狀態'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨狀態: {purstate}"}
                    ]
                },
            }

            # 添加一个额外的按钮选项
            bubble["footer"] = {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "商品已到貨",
                            "text": f"商品已到貨 {pid}"  # 根据需要调整文本
                        }
                    }
                ]
            }

            bubbles.append(bubble)

        flex_message = FlexSendMessage(alt_text="此商品進貨中列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品進貨中列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message


def pured_pro_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0]  # '商品ID'
            pname = row[1]  # '商品名稱'
            purstate = row[2]  # '進貨狀態'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"商品名稱: {pname}"},
                        {"type": "text", "text": f"進貨狀態: {purstate}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message

def order_inf_flex_msg(result):
    if result is not None:
        bubbles = []
        for row in result:
            pid = row[0] # '商品ID'
            ordernum = row[1] # '訂單編號'
            orderstate = row[2] # '訂單狀態未取已取'
            bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"商品ID: {pid}"},
                        {"type": "text", "text": f"訂單編號: {ordernum}"},
                        {"type": "text", "text": f"訂單狀態: {orderstate}"}
                    ]
                },
            }
            bubbles.append(bubble)
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "carousel", "contents": bubbles})
    else:
        flex_message = FlexSendMessage(alt_text="此商品已到貨列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})
    return flex_message




