from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
import lineboterp
from database  import *

#-------------------未取列表----------------------
def ordernottaken_list():
    db_nottaken = ordertoplist()
    if db_nottaken=='找不到符合條件的資料。':
        ordernottaken_show = TextSendMessage(text='您尚未有未取資料')
    else:
        ordernottaken_show = []#發送全部
        ordernottaken_handlelist = []#處理切割db_nottaken資料10筆一組

        # 迴圈每次取出10個元素，並將這兩個元素作為一個子陣列存入結果陣列中，直到取完為止
        while len(db_nottaken) > 0:
            two_elements = db_nottaken[:10]  # 取得10個元素
            ordernottaken_handlelist.append(two_elements)  # 將10個元素作為一個子陣列加入結果陣列
            db_nottaken = db_nottaken[10:]  # 移除已取得的元素

        for totallist in ordernottaken_handlelist:
            buttons = []  # #模塊中10筆資料
            for i in range(len(totallist)):
                lumpsum = totallist[i][1]
                if lumpsum is not None:
                    lumpsum_formatted = '{:,}'.format(lumpsum)
                dtime = totallist[i][2].strftime('%Y-%m-%d %H:%M')
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"[{dtime}] NT${lumpsum_formatted}",
                        "text": f"【訂單詳細】{dtime}\n{totallist[i][0]}"
                    },
                    "color": "#FF8C00"
                }
                buttons.append(button)

            ordernottaken_show.append({
                    "type": "bubble",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "高逸嚴選",
                        "weight": "bold",
                        "color": "#A44528",
                        "size": "sm"
                        },
                        {
                        "type": "text",
                        "text": "未取訂單查詢",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                        },
                        {
                        "type": "separator",
                        "margin": "xxl"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": buttons
                        }
                    ]
                    },
                    "styles": {
                    "footer": {
                        "separator": True
                    }
                    }
                })
        
        ordernottaken_show = FlexSendMessage(
            alt_text="未取訂單查詢",
            contents={
                "type": "carousel",
                "contents": ordernottaken_show      
                } 
            )
    return ordernottaken_show

#-------------------預購列表----------------------
def orderpreorder_list():
    db_nottaken = orderpreorderlist()
    if db_nottaken=='找不到符合條件的資料。':
        orderpreorder_show = TextSendMessage(text='您尚未有未取資料')
    else:
        orderpreorder_show = []#發送全部
        orderpreorder_handlelist = []#處理切割db_nottaken資料10筆一組

        # 迴圈每次取出10個元素，並將這兩個元素作為一個子陣列存入結果陣列中，直到取完為止
        while len(db_nottaken) > 0:
            two_elements = db_nottaken[:10]  # 取得10個元素
            orderpreorder_handlelist.append(two_elements)  # 將10個元素作為一個子陣列加入結果陣列
            db_nottaken = db_nottaken[10:]  # 移除已取得的元素

        for totallist in orderpreorder_handlelist:
            buttons = []  # #模塊中10筆資料
            for i in range(len(totallist)):
                lumpsum = totallist[i][1]
                if lumpsum is not None:
                    lumpsum_formatted = '{:,}'.format(lumpsum)
                dtime = totallist[i][2].strftime('%Y-%m-%d %H:%M')
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"[{dtime}] NT${lumpsum_formatted}",
                        "text": f"【訂單詳細】{dtime}\n{totallist[i][0]}"
                    },
                    "color": "#fe587b"
                }
                buttons.append(button)

            orderpreorder_show.append({
                    "type": "bubble",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "高逸嚴選",
                        "weight": "bold",
                        "color": "#A44528",
                        "size": "sm"
                        },
                        {
                        "type": "text",
                        "text": "預購訂單查詢",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                        },
                        {
                        "type": "separator",
                        "margin": "xxl"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": buttons
                        }
                    ]
                    },
                    "styles": {
                    "footer": {
                        "separator": True
                    }
                    }
                })
        
        orderpreorder_show = FlexSendMessage(
            alt_text="預購訂單查詢",
            contents={
                "type": "carousel",
                "contents": orderpreorder_show      
                } 
            )
    return orderpreorder_show
#-------------------歷史列表----------------------
def orderhastaken_list():
    db_hastaken = ordertopalllist()
    if db_hastaken=='找不到符合條件的資料。':
        orderhastaken_show = TextSendMessage(text='您尚未有完成歷史資料')
    else:
        orderhastaken_show = []#發送全部
        orderhastaken_handlelist = []#處理切割db_nottaken資料10筆一組

        # 迴圈每次取出10個元素，並將這兩個元素作為一個子陣列存入結果陣列中，直到取完為止
        while len(db_hastaken) > 0:
            two_elements = db_hastaken[:10]  # 取得10個元素
            orderhastaken_handlelist.append(two_elements)  # 將10個元素作為一個子陣列加入結果陣列
            db_hastaken = db_hastaken[10:]  # 移除已取得的元素

        for totallist in orderhastaken_handlelist:
            buttons = []  # #模塊中10筆資料
            for i in range(len(totallist)):
                lumpsum = totallist[i][1]
                if lumpsum is not None:
                    lumpsum_formatted = '{:,}'.format(lumpsum)
                dtime = totallist[i][2].strftime('%Y-%m-%d %H:%M')
                button = {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"[{dtime}] NT${lumpsum_formatted}",
                        "text": f"【訂單詳細】{dtime}\n{totallist[i][0]}"
                    },
                    "color": "#8FBC8F"
                }
                buttons.append(button)

            orderhastaken_show.append({
                    "type": "bubble",
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "高逸嚴選",
                        "weight": "bold",
                        "color": "#A44528",
                        "size": "sm"
                        },
                        {
                        "type": "text",
                        "text": "已完成訂單列表",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                        },
                        {
                        "type": "separator",
                        "margin": "xxl"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": buttons
                        }
                    ]
                    },
                    "styles": {
                    "footer": {
                        "separator": True
                    }
                    }
                })
        
        orderhastaken_show = FlexSendMessage(
            alt_text="已完成訂單列表",
            contents={
                "type": "carousel",
                "contents": orderhastaken_show      
                } 
            )
    return orderhastaken_show

#-------------------訂單詳細資料----------------------
def orderdtsearch():
    db_orderdt = orderdt()
    if db_orderdt=='找不到符合條件的資料。':
        show = TextSendMessage(text=db_orderdt)
    else:
        '''訂單編號,電話,訂單狀態未取已取,商品ID,商品名稱,商品單位,訂購數量,商品小計,總額,訂單成立時間,取貨完成時間'''
        showdt = [] #訊息中的內容儲存
        if db_orderdt[0][10] is None:
            pickup = '無資料'
        else:
            pickup = str(db_orderdt[0][10])
            
        if db_orderdt[0][2] in ['未取','預購','預購未取']:
            ordertype = db_orderdt[0][2]
            if db_orderdt[0][2] == '未取':
                text = '已經可以前往「店面取貨」囉～'
            elif db_orderdt[0][2] == '預購':
                text = '預購商品尚未到店！'
            elif db_orderdt[0][2] == '預購未取':
                text = '預購商品已到店囉！\n已經可以前往「店面取貨」囉～'
            msg = {
                        "type": "text",
                        "text": f"\n{text}",
                        "wrap": True,
                        "color": "#fb5840",##顏色換
                        "size": "md",
                        "flex": 5,
                        "margin": "none",
                        "weight": "bold",
                        "align": "center"
                    }
        else:
            ordertype = '歷史'
            msg = {
                        "type": "text",
                        "text": "\n感謝您的訂購！",
                        "wrap": True,
                        "color": "#fb5840",##顏色換
                        "size": "md",
                        "flex": 5,
                        "margin": "none",
                        "weight": "bold",
                        "align": "center"
                    }

        items = len(db_orderdt)#項數
        pieces = 0
        for piecesadd in db_orderdt:
            pieces += piecesadd[6]

        show1 = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "高逸嚴選",
                        "color": "#A44528",
                        "size": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "訂單摘要",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "margin": "xl",
                        "color": "#010203"
                    },
                    {
                        "type": "separator",
                        "color": "#010203",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"◇訂單編號：{str(db_orderdt[0][0])}",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "md",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇成立時間：{str(db_orderdt[0][9])}",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "sm",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇訂單狀態：{db_orderdt[0][2]}",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "md",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇電話號碼：{str(db_orderdt[0][1])}",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "sm",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇商品項數：{items}項",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "sm",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇商品件數：{pieces}件",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "sm",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "text",
                        "text": f"◇訂單總計：NT${str('{:,}'.format(db_orderdt[0][8]))}",
                        "weight": "bold",
                        "size": "md",
                        "align": "start",
                        "margin": "sm",
                        "offsetStart": "10px",
                        "color": "#3b5a5f"
                    },
                    {
                        "type": "separator",
                        "color": "#010203",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"☆取貨/取消時間：{pickup}",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "sm",
                        "offsetStart": "10px"
                    },
                    {
                        "type": "text",
                        "text": f"<<詳細資訊共{items}頁>>",
                        "size": "sm",
                        "align": "end",
                        "margin": "md"
                    },
                    msg
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": f"繼續瀏覽{ordertype}訂單列表",
                        "text": f"{ordertype}訂單列表"#預購/歷史
                        },
                        "color": "#A44528"
                    }
                    ],
                    "flex": 0
                }
                }
        showdt.append(show1)
        num = 0
        while len(db_orderdt) > 0:
            num += 1
            discount = onlyprice(db_orderdt[0][3])
            if db_orderdt[0][6] >= 2:
                if discount == '(優惠價)':
                    discount = '(優惠價)'
                else:
                    discount = ''
            else:
                discount = ''
            price = int(db_orderdt[0][7] / db_orderdt[0][6])

            show2 = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "高逸嚴選",
                            "color": "#A44528",
                            "size": "sm",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"詳細資訊({num}/{items})",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "margin": "xl",
                            "color": "#010203"
                        },
                        {
                            "type": "separator",
                            "color": "#010203",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "xs",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇商品編號：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{db_orderdt[0][3]}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇商品名稱：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{db_orderdt[0][4]}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇商品單價：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"每{db_orderdt[0][5]}{price}元{discount}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "◇現購數量：",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ],
                                    "width": "100px"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{db_orderdt[0][6]}{db_orderdt[0][5]}",
                                        "wrap": True,
                                        "color": "#3b5a5f",
                                        "size": "md",
                                        "flex": 5,
                                        "margin": "sm",
                                        "weight": "bold"
                                    }
                                    ]
                                }
                                ]
                            }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xl",
                            "color": "#010203"
                        },
                        {
                            "type": "text",
                            "text": f"小計：NT${str('{:,}'.format(db_orderdt[0][7]))}",
                            "wrap": True,
                            "color": "#3b5a5f",
                            "size": "lg",
                            "flex": 5,
                            "margin": "sm",
                            "weight": "bold",
                            "align": "end"
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
                            "style": "primary",
                            "height": "sm",
                            "action": {
                            "type": "message",
                            "label": f"繼續瀏覽{ordertype}訂單列表",
                            "text": f"{ordertype}訂單列表"#預購/歷史
                            },
                            "color": "#A44528"
                        }
                        ],
                        "flex": 0
                    }
                    }
            db_orderdt = db_orderdt[1:]  # 移除已取得的元素
            showdt.append(show2)

        show = FlexSendMessage(
            alt_text=f"{ordertype}訂單詳細資訊",
            contents={
                "type": "carousel",
                "contents": showdt     
                } 
            )
    return show