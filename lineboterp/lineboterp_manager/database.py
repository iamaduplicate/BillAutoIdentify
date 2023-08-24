from linebot.models import FlexSendMessage
import mysql.connector
import requests
from datetime import datetime, timedelta
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import dbinfo,imgurinfo
import os, io, pyimgur, glob
import manager
#安裝 Python 的 MySQL 連接器及其相依性>pip install mysql-connector-python
#安裝Python 的 pyimgur套件> pip install pyimgur
# Obtain connection string information from the portal

#-------------------舊資料庫連線----------------------
def databasetest():
  #取得資料庫資訊
  dbdata = dbinfo()  
  config = {
  'host': dbdata['host'],
  'user': dbdata['user'],
  'password': dbdata['password'],
  'database': dbdata['database']
  }
  # Construct connection string
  try:
    conn = mysql.connector.connect(**config)
    databasetest_msg = '資料庫連接成功'
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      databasetest_msg = '使用者或密碼有錯'
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      databasetest_msg = '資料庫不存在或其他錯誤'
    else:
      databasetest_msg = err
  else:
    cursor = conn.cursor()
  return {'databasetest_msg': databasetest_msg, 'conn':conn, 'cursor':cursor, 'config':config}
#----------------查詢資料庫裡所有廠商編號及廠商名--------------------
def test_manufacturers():
    testimplement = databasetest()
    conn = testimplement['conn']
    cursor = testimplement['cursor']
    query = "SELECT * FROM Manufacturer_Information;"
    cursor.execute(query)
    result = cursor.fetchall()
    
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
                    "text": "【商品查詢1】查詢",
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
                            "text": f"【廠商的編號】: {mid}",
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
                      "text": f"選擇廠商 {mid}"
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
    
    cursor.close()
    conn.close()
    return flex_message

def products_manufacturers(manufacturer_id):
    testAimplement = databasetest()
    conn = testAimplement['conn']
    cursor = testAimplement['cursor']
    query = f"SELECT * FROM Manufacturer_Information NATURAL JOIN Product_information WHERE 廠商編號 = '{manufacturer_id}'"
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        bubbles = []
        for row in result:
            pid = row[9]  # '商品ID'
            pname = row[10]  # '商品名稱'
            stock_num = row[14]  # '庫存數量'
            sell_price = row[16]  # '售出單價'

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

    cursor.close()
    conn.close()
    return flex_message


#-----------分類下的所有商品-----------
def test_categoryate(selected_category):
    testBimplement = databasetest()
    conn = testBimplement['conn']
    cursor = testBimplement['cursor']
    query = f"SELECT 商品ID, 商品名稱 FROM Product_information WHERE 商品ID LIKE '{selected_category}%'"
    cursor.execute(query)
    result = cursor.fetchall()

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
                        {"type": "text", "text": f"商品名稱：{pname}"}
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

    cursor.close()
    conn.close()
    return flex_message


#查詢資料SELECT
def test_datasearch():
  #測試讀取資料庫願望清單(所有)
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = "SELECT * FROM wishlist;"
  cursor.execute(query)
  result = cursor.fetchall()
  if result is not None:
    testmsg = "願望清單讀取內容：\n"
    for row in result:
      # 透過欄位名稱獲取資料
      uid = row[0]#'UID'
      name = row[1]#'商品名稱'
      #商品圖片
      reason = row[3]#'推薦原因'
      time = row[4]#'願望建立時間'
      member = row[5]#'會員_LINE_ID'
      # 在這裡進行資料處理或其他操作
      testmsg += ('第%s筆\n推薦會員:\n%s\n商品名稱：\n%s\n推薦原因：\n%s\n願望建立時間：\n%s\n---\n' %(uid,member,name,reason,time))
  else:
    testmsg = "找不到符合條件的資料。"
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg


#-------------------圖片取得並發送----------------------
def imagesent():
    implement = databasetest()  # 定義 databasetest() 函式並返回相關物件 #要
    img = []
    send = []
    conn = implement['conn'] #要
    cursor = implement['cursor'] #要
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;" #要
    cursor.execute(query) #要
    result = cursor.fetchall() #要
    
    if result is not None:
        for row in result:
            productname = row[0] # 圖片商品名稱
            output_path = row[1] # 圖片連結
            # 發送圖片
            text_msg = TextSendMessage(text=productname)
            image_msg = ImageSendMessage(
                original_content_url=output_path,  # 圖片原圖
                preview_image_url=output_path  # 圖片縮圖
            )
            img.append(text_msg)
            img.append(image_msg)
    else:
        img.append(TextSendMessage(text='找不到符合條件的資料。'))
    
    # 關閉游標與連線
    cursor.close()
    conn.close()
    send = tuple(img)  # 將列表轉換為元組最多五個
    return send

#-------------------刪除images資料夾中所有----------------------
def delete_images():
    folder_path = 'images'  # 資料夾路徑
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"已刪除圖片檔案：{file_path}")

#-------------------images資料夾中圖片轉連結----------------------
def imagetolink():
  imgurdata = imgurinfo()
  image_storage = []
  folder_path = 'images'# 設定資料夾路徑
  # 使用 glob 模組取得資料夾中的 JPG 和 PNG 圖片檔案
  image_files = glob.glob(f"{folder_path}/*.jpg") + glob.glob(f"{folder_path}/*.png")
  # 讀取所有圖片檔案
  for file in image_files:
    # 獲取檔案名稱及副檔名
    filename, file_extension = os.path.splitext(file)
    filename = filename+file_extension# 檔案位置加副檔名
    image_storage.append(filename)

  #執行轉換連結
  for img_path in image_storage:
    CLIENT_ID = imgurdata['CLIENT_ID_data']
    PATH = img_path #A Filepath to an image on your computer"
    title = img_path
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    #image = uploaded_image.title + "連結：" + uploaded_image.link
    imagetitle = uploaded_image.title
    imagelink = uploaded_image.link
    print( imagetitle + "連結：" + imagelink)
    #delete_images()#刪除images檔案圖片
  return {'imagetitle':imagetitle,'imagelink':imagelink}


#查詢並列出所有廠商名稱
def manufacturers(mid,mname):
  conn = manager.db['conn']
  cursor = manager.db['cursor']
  query = f"""select * from Manufacturer_Information"""
  cursor.execute(query)
  result = cursor.fetchall()

#關閉查詢游標及關閉連線
  cursor.close()
  conn.close()

  if result is not None:
    testmsg = "所有廠商如下：\n"
    for row in result:
      # 透過欄位名稱獲取資料
      mid = row[0]#'廠商編號'
      mname = row[1]#'廠商名'
      # 在這裡進行資料處理或其他操作
      testmsg += f'廠商編號:\n{mid}\n廠商名：\n{mname}\n'
  else:
    testmsg = "找不到符合條件的資料。"

  testmsg += "(end)"
  return testmsg