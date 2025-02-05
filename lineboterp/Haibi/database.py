import mysql.connector
import requests
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

#-------------------資料庫連線----------------------
def databasetest():
  #取得資料庫資訊
  db = manager.db
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
  db['conn'] = conn
  db['cursor'] = cursor
  db['databasetest_msg'] = databasetest_msg
  

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

#修改資料UPDATE
def test_dataUPDATE():
  return

#-------------------圖片取得並發送----------------------
def imagesent():
    implement = databasetest()  # 定義 databasetest() 函式並返回相關物件
    img = []
    send = []
    conn = implement['conn']
    cursor = implement['cursor']
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;"
    cursor.execute(query)
    result = cursor.fetchall()
    
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

#-------------------取出預購名單---------------------------------
def preorder_list():
  cursor = manager.db['cursor']
  query = f"""
          SELECT 訂單編號, 會員_LINE_ID, 電話, 訂單成立時間, 總額
          FROM Order_information
			    WHERE 訂單狀態未取已取='預購';"""
  cursor.execute(query)
  result = cursor.fetchall()
  if result != []:
    orderlist = result
  else:
    orderlist = "找不到符合條件的資料。"
  return orderlist
#-------------------取出未取名單---------------------------------
def order_list():
  cursor = manager.db['cursor']
  query = f"""
          SELECT 訂單編號, 會員_LINE_ID, 電話, 訂單成立時間, 總額
          FROM Order_information
			    WHERE 訂單狀態未取已取='預購未取' or 訂單狀態未取已取='現購未取'
          limit 100 offset 0;"""
  cursor.execute(query)
  result = cursor.fetchall()
  if result != []:
    orderlist = result
  else:
    orderlist = "找不到符合條件的資料。"
  return orderlist
#-------------------訂單詳細資料------------------------
def orderdt():
  userid = manager.user_id
  ordersearch = manager.orderall[userid+'dt'] #本是使用者的ID
  cursor = manager.db['cursor']
  query = f"""
          SELECT
            Order_information.訂單編號,
            Order_information.電話,
            Order_information.訂單狀態未取已取,
            Product_information.商品ID,
            Product_information.商品名稱,
            Product_information.商品單位,
            order_details.訂購數量,
            order_details.商品小計,
            Order_information.總額,
            Order_information.訂單成立時間,
            Order_information.取貨完成時間
          FROM
            Order_information
          JOIN
            order_details ON Order_information.訂單編號 = order_details.訂單編號
          JOIN
            Product_information ON order_details.商品ID = Product_information.商品ID
          WHERE Order_information.訂單編號 = '{ordersearch}' ;
          """
  cursor.execute(query)
  result = cursor.fetchall()
  if result == []:
    result = '找不到符合條件的資料。'
  return result
#-------------------取出庫存---------------------------------
def inquiry_list():
  cursor = manager.db['cursor']
  query = """
    SELECT 商品名稱, 商品ID, 庫存數量
    FROM Product_information
    WHERE 現預購商品='現購'
    order by 庫存數量 asc;"""
  cursor.execute(query)
  result = cursor.fetchall()
  if result != []:
    report = result
  else:
    report = "找不到符合條件的資料。"
  return report