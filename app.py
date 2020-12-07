#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
from bs4 import BeautifulSoup 
import json,codecs
import zdict
import subprocess,os,tempfile,re
from gne import GeneralNewsExtractor
from gtts import gTTS
import pyrebase
import tracemoepy
import pyimgur

CLIENT_ID = "請填入Imgur Client ID"

config={
    "apiKey": "Firebase",
    "authDomain": "Firebase",
    "databaseURL": "Firebase",
    "projectId": "Firebase",
    "storageBucket": "Firebase",
    "messagingSenderId": "Firebase",
    "appId": "Firebase",
    "measurementId": "Firebase"
}

setting = {
    "sauce": False,
    "moe":False,
    "lockURL":False
}

im = pyimgur.Imgur(CLIENT_ID)
tracemoe = tracemoepy.tracemoe.TraceMoe()
session = requests.session()
extractor = GeneralNewsExtractor()
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('填入LineBot Token')
# Channel Secret
handler = WebhookHandler('填入LinBot Secret')

    
def helpmessage():
    helpMessage = """«指令表»
⇒【help】幫助
⇒【天氣 [縣市名]】查詢天氣
⇒【/字典 [字詞]】字典小助手
⇒【/語音 [語言] [字詞]】Google語音
⇒【/繁化 [模式] [字詞]】繁化姬助理
⇒【/搜圖 [on/off]】搜圖開關
⇒【/moe】[on/off]動漫截圖搜尋開關
⇒【/covid】[ISO code] Covid-19

搜圖與moe將會在上傳圖片後關閉✔
丟新聞網址會自動提取內文✔
支持多家 多國媒體✔

«狀態表»
搜圖狀態:{}
moe狀態:{}
限制新聞內文提取功能:{}""".format(setting["sauce"],setting["moe"],setting["lockURL"])

    return helpMessage 

num = 0
CityList=["宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","屏東縣"]

def getWeather(city):
	path = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-089?Authorization=CWB-8F001719-D827-4247-B4C2-7251BB99B8A0&locationName={}'.format(city)
	resp = requests.get(path)
	list = json.loads(resp.text)
	temp = list['records']['locations'][0]['location']
	weather=[]
	for data in range(0,len(temp)):
		Name=temp[data]['locationName']
		weatherElement=temp[data]['weatherElement']
		data=weatherElement[6]['time']
		data0=weatherElement[3]['time'][0]['elementValue'][0]['value']
		startTime = weatherElement[6]['time'][0]['startTime']
		endTime = weatherElement[6]['time'][0]['endTime']
		elementValue = weatherElement[6]['time'][0]['elementValue']
		entries = elementValue[0]['value']
		WHList=entries.split('。')
		a = "{} ==> 天氣{} (時間：{} ~ {})\n============== \n{} 體感溫度攝氏{}度 \n============== \n{} {} \n============== \n{} {} \n\n".format(Name,WHList[0],startTime,endTime,WHList[2],data0,WHList[5],WHList[3],WHList[1],WHList[4])
		#print("%s ==> 天氣%s (時間：%s ~ %s)\n============== \n%s 體感溫度攝氏%s度 \n============== \n%s %s \n============== \n%s %s \n\n"%(Name,WHList[0],startTime,endTime,WHList[2],data0,WHList[5],WHList[3],WHList[1],WHList[4]))
		weather.append(a)
	return weather

def zhconvert(converter,text):
    path = "https://api.zhconvert.org/convert?converter={}&text={}&prettify=1".format(converter,text)
    resp = requests.get(path)
    json_list = json.loads(resp.text)
    text = json_list["data"]["text"]
    return text

data = {
    "name": "Vincent9579",
    "number" : 28
}

def upload_data(data):
    fb=pyrebase.initialize_app(config)
    db = fb.database()
    db.child("users").push(data)

def upload(path_on_cloud,path_local):
    fb=pyrebase.initialize_app(config)
    storage=fb.storage()
    storage.child(path_on_cloud).put(path_local)

def saucenao(photo_url):
    try:
        url="https://saucenao.com/search.php"
        #url = "https://saucenao.com"
        Header = {
            'Host': 'saucenao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept - Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept - Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive'

        }
        payloaddata = {

            'frame': 1,
            'hide': 0,
            'database': 999,
        }
        #files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        photo_file=requests.get(photo_url)
        files = {"file": (
        "saucenao.jpg", photo_file.content, "image/png")}
        print("正在搜尋...")
        r = session.post(url=url, headers=Header, data=payloaddata,files=files)
        #r = session .get(url=url,headers=Header)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup.prettify())
        result=0
        choice=0
        for img in soup.find_all('div', attrs={'class': 'result'}):  # 找到class="wrap"的div里面的所有<img>标签
            #print(img)
            if('hidden' in str(img['class']))==False:
                try:
                    name=img.find("div",attrs={'class': 'resulttitle'}).get_text()
                    img_url=str(img.img['src'])
                    describe_list=img.find("div",attrs={'class': 'resultcontentcolumn'})
                    url_list = img.find("div", attrs={'class': 'resultcontentcolumn'}).find_all("a",  attrs={'class': 'linkify'})
                    similarity = str(img.find("div", attrs={'class': 'resultsimilarityinfo'}).get_text())
                    print(name)
                except:
                    continue
                try:
                    describe = str(url_list[0].previous_sibling.string)
                    describe_id = str(url_list[0].string)
                    describe_url = str(url_list[0]['href'])
                    auther_url = str(url_list[1]['href'])
                    auther = str(url_list[1].previous_sibling.string)
                    auther_id = str(url_list[1].string)
                    '''print(name)
                    print(img_url)
                    print(describe)
                    print(describe_id)
                    print(similarity)
                    print(auther)
                    print(auther_id)
                    print(describe_url)'''
                    text = f"{name}\n{describe}[{describe_id}]({describe_url})\n{auther}:[{auther_id}]({auther_url})\n相似度{similarity}"
                except:
                    '''print(describe_list.get_text())
                    print(describe_list.strong.string)
                    print(describe_list.strong.next_sibling.string)
                    print(describe_list.small.string)
                    print(describe_list.small.next_sibling.next_sibling.string)'''
                    auther = str(describe_list.strong.string)
                    auther_id = str(describe_list.strong.next_sibling.string)
                    describe = str(describe_list.small.string) + "\n" + str(describe_list.small.next_sibling.next_sibling.string)
                    text = f"{name}\n{auther}:{auther_id}\n{describe}\n相似度{similarity}"

                photo_file = session.get(img_url)
                

                result=1
                return text
        if result==0:
            text="SauceNAO:找無圖片"
            return text
    except:
        texts="SauceNAO:錯誤"
        return texts

def ascii2d(photo_url):
    try:
        url = "https://ascii2d.net/"
        texts=[]
        # url = "https://saucenao.com"
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'
        }
        html = session.get(url, headers=Header)
        print(html)
        authenticity_token = re.findall("<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*?)\" />", html.text, re.S)[0]
        payloaddata = {

            'authenticity_token': authenticity_token,
            'utf8': "✓",
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        print("正在搜索ascii2d")
        photo_file = requests.get(photo_url)
        files = {"file": (
            "saucenao.jpg", photo_file.content, "image/png")}
        url = "https://ascii2d.net/search/multi"
        r = session.post(url=url, headers=Header, data=payloaddata, files=files)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        pan = 0
        for img in soup.find_all('div', attrs={'class': 'row item-box'}):  # 找到class="wrap"的div里面的所有<img>标签
            # print(img)
            if pan != 0:
                img_url = "https://ascii2d.net" + str(img.img['src'])
                the_list = img.find_all('a')
                title = str(the_list[0].get_text())
                title_url = str(the_list[0]["href"])
                auther = str(the_list[1].get_text())
                auther_url = str(the_list[1]["href"])

                photo_file = session.get(img_url)
                text=f"標題:[{title}]({title_url})\n作者:[{auther}]({auther_url})"
                texts.append(text)
                print(text)
            pan = pan + 1
            if pan == 3:
                break
        return texts
    except Exception  as e:
        print(e)

def covid(CountryName):
    path = "https://disease.sh/v3/covid-19/countries/{}".format(CountryName)
    resp = requests.get(path)
    json_list = json.loads(resp.text)
    length = len(json_list)
    if length != 1:
        Country = json_list["country"]
        CountryInfo = json_list["countryInfo"]
        iso2 = CountryInfo["iso2"]
        iso3 = CountryInfo["iso3"]
        flag = CountryInfo["flag"]
        todayCases = json_list["todayCases"]
        cases = json_list["cases"]
        deaths = json_list["deaths"]
        todayDeaths = json_list["todayDeaths"]
        recovered = json_list["recovered"]
        todayRecovered = json_list["todayRecovered"]
        active = json_list["active"]
        critical = json_list["critical" ]
        CovidMessage = """«COVID-19即時狀況»
國家名稱 ⇒ {}
ISO代碼 ⇒ {},{}
今日確診人數 ⇒ {}
今日死亡人數 ⇒ {}
今日痊癒人數 ⇒ {}
尚未痊癒人數 ⇒ {}
累計確診人數 ⇒ {}
累計死亡人數 ⇒ {}
累計痊癒人數 ⇒ {}
病危人數 ⇒ {}
""".format(Country,iso2,iso3,todayCases,todayDeaths,todayRecovered,active,cases,deaths,recovered,critical)
        return CovidMessage
    else:
        return "查無此國家資料"

   
@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask!</h1>"

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

# 處理訊息
@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    #print(event)
    if isinstance(event.message, TextMessage):
        text = event.message.text
        help_str = ['help','幫助','功能']
        if text.lower() in help_str:
            helpmessagea = helpmessage()
            text_message = TextSendMessage(text=str(helpmessagea),
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="天氣", text="天氣")),
                                   QuickReplyButton(action=MessageAction(label="/字典", text="/字典")),
                                   QuickReplyButton(action=MessageAction(label="/翻譯", text="/covid")),
                                   QuickReplyButton(action=MessageAction(label="/語音", text="/語音")),
                                   QuickReplyButton(action=MessageAction(label="/繁化", text="/繁化"))
                               ]))
            line_bot_api.reply_message(event.reply_token, text_message)
        if text.startswith("天氣"):
            if text.replace("天氣","") == "":
                message = TextSendMessage(text="請輸入縣市名稱\n格式:天氣 {縣市名稱}")
                line_bot_api.reply_message(event.reply_token, message)
            if text.replace("天氣 ","") in CityList:
                text_city = text.replace("天氣 ","")
                WeatherList1 = getWeather(text_city)
                for i in range (0,len(WeatherList1)):
                    data = WeatherList1[i]
                    message = TextSendMessage(text=data)
                    line_bot_api.reply_message(event.reply_token, message)
            if text.replace("天氣 ","") == "台北市":
                WeatherList1 = getWeather("臺北市")
                for i in range (0,len(WeatherList1)):
                    data = WeatherList1[i]
                    message = TextSendMessage(text=data)
                    line_bot_api.reply_message(event.reply_token, message)
            else:
                message = TextSendMessage(text="輸入格式錯誤\n格式:天氣 {縣市名稱}")
                line_bot_api.reply_message(event.reply_token, message) 
        if text.lower().startswith("/covid"):
            if text.lower().replace("/covid","") == "":
                message = TextSendMessage(text="請輸入國家名稱或其ISO代碼\n/covid:天氣 {國家名稱orISO代碼}")
                line_bot_api.reply_message(event.reply_token, message)
            if len(text.split(" ")) == 2:
                txt = text.lower().split(" ")
                Country = txt[1]
                CovidMessage = covid(Country)
                message = TextSendMessage(text=CovidMessage)
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = TextSendMessage(text="輸入格式錯誤\n請輸入國家名稱或其ISO代碼\n/covid:天氣 {國家名稱orISO代碼}")
                line_bot_api.reply_message(event.reply_token, message)
        if text.startswith("/字典"):
            if text.replace("/字典","") == "":
                message = TextSendMessage(text="請輸入要查詢的字詞\n格式:/字典 {字典} {查詢字詞}\n字典可為空\n可用字典有:\n預設:Yahoo字典\nmoe:萌典\nurban:Urban\nspanish:SpanishDict\njisho:Jisho Japanese Dictionary\nyandex:Yandex Translate\nwiktionary:Wiktionary\nitaigi:iTaigi-愛台語\nnaer:國家教育研究院\napc:原住民族語言線上詞典")
                line_bot_api.reply_message(event.reply_token, message)  
            if len(text.split(" ")) == 2:
                out_text = text.replace("/zdict","")
                command = "zdict -V {}".format(out_text)
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
                p.wait()
                result_lines = p.stdout.readlines() 
                result = ""
                for line in result_lines:
                    print(line.strip()) 
                    result += line.strip()
                    result += "\n"
                message = TextSendMessage(text=result)
                line_bot_api.reply_message(event.reply_token, message) 
            if len(text.split(" ")) == 3:
                choose_dict=["預設","moe","urban","spanish","jisho","yandex","wiktionary","itaigi","naer","apc"]
                text_split=text.split(" ")
                if text_split[1] in choose_dict:
                    text_dict = text_split[1]
                    text_word = text_split[2]
                    command = "zdict --dict {} -V {}".format(text_dict,text_word)
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
                    p.wait()
                    result_lines = p.stdout.readlines() 
                    result = ""
                    for line in result_lines:
                        print(line.strip()) 
                        result += line.strip()
                        result += "\n"
                    message = TextSendMessage(text=result)
                    line_bot_api.reply_message(event.reply_token, message) 
                else:
                    text_word = text_split[2]
                    command = "zdict -V {}".format(text_word)
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True) 
                    p.wait()
                    result_lines = p.stdout.readlines() 
                    result = "因輸入不支援的字典,採用預設字典\n"
                    for line in result_lines:
                        print(line.strip()) 
                        result += line.strip()
                        result += "\n"
                    message = TextSendMessage(text=result)
                    line_bot_api.reply_message(event.reply_token, message) 
        if text.startswith("https://"):     
            url = text.replace("https://","") 
            url_head = url.split("/")[0]
            support_site = ["today.line.me","www.msn.com","udn.com","news.ltn.com.tw","www.ltn.com.tw","tw.news.yahoo.com","www.chinatimes.com","news.tvbs.com.tw","www.ftvnews.com.tw","news.ebc.net.tw","www.setn.com","www.storm.mg","liff.line.me"]
            if setting["lockURL"] == True:
                if url_head in support_site:
                    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
                    html = requests.get(text,headers = headers)
                    html.encoding = 'utf-8'
                    result = extractor.extract(html.text)
                    text = "{}\n\n{}".format(result["title"],result["content"])
                    if len(text) >= 4990:
                        message = TextSendMessage(text="超過5000字 無法傳送")
                    else:
                        message = TextSendMessage(text=text)
                        line_bot_api.reply_message(event.reply_token, message) 
            else:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
                html = requests.get(text,headers = headers)
                html.encoding = 'utf-8'
                result = extractor.extract(html.text)
                text = "{}\n\n{}".format(result["title"],result["content"])
                if len(text) >= 4990:
                    message = TextSendMessage(text="超過5000字 無法傳送")
                else:
                    message = TextSendMessage(text=text)
                    line_bot_api.reply_message(event.reply_token, message) 

        if text.startswith("/繁化"):
            if text.replace("/繁化","") == "":
                message = TextSendMessage(text="請輸入要繁化的字詞\n格式:/繁化 {轉換器} {被轉換的文字}\n轉換器有 \nSimplified （簡體化）、 Traditional （繁體化）、 China （中國化）、 Hongkong （香港化）、 Taiwan （台灣化）、 Pinyin （拼音化） Bopomofo （注音化）、 Mars （火星化）、 WikiSimplified （維基簡體化）、 WikiTraditional （維基繁體化）。")
                line_bot_api.reply_message(event.reply_token, message)   
            if len(text.split(" ")) == 2:
                message = TextSendMessage(text="錯誤\n請按照正確格式輸入\n格式:/繁化 {轉換器} {被轉換的文字}\n轉換器有 \nSimplified （簡體化）、 Traditional （繁體化）、 China （中國化）、 Hongkong （香港化）、 Taiwan （台灣化）、 Pinyin （拼音化） Bopomofo （注音化）、 Mars （火星化）、 WikiSimplified （維基簡體化）、 WikiTraditional （維基繁體化）。")
                line_bot_api.reply_message(event.reply_token, message)      
            if len(text.split(" ")) == 3:
                converter = text.split(" ")[1]
                txt = text.split(" ")[2]
                zh = zhconvert(converter,txt)
                message = TextSendMessage(text=zh)
                line_bot_api.reply_message(event.reply_token, message)  
        if text.startswith("/語音"):
            if text.replace("/語音","") == "":
                message = TextSendMessage(text="請輸入要輸出的字詞\n格式:/語音_{輸出語言}_{字詞}\n若輸出語言為空，則以zh-tw輸出")
                line_bot_api.reply_message(event.reply_token, message)   
            if len(text.split("_")) == 2:
                lang = 'zh-tw' 
                txt = text.split("_")[1]
                tts = gTTS(txt, lang=lang)
                tts.save("hasil.mp3")
                path_local = "hasil.mp3"
                upload(path_local,path_local)
                audio_message=AudioSendMessage(original_content_url="https://firebasestorage.googleapis.com/v0/b/fbclass-7e786.appspot.com/o/hasil.mp3?alt=media&token=none",duration=330*len(txt))
                line_bot_api.reply_message(event.reply_token, audio_message)   
            if len(text.split("_")) == 3:
                lang = text.split("_")[1]
                txt = text.split("_")[2]
                tts = gTTS(txt, lang=lang)
                tts.save("hasil.mp3")
            
                path_local = "hasil.mp3"
                upload(path_local,path_local)
                audio_message=AudioSendMessage(original_content_url="https://firebasestorage.googleapis.com/v0/b/fbclass-7e786.appspot.com/o/hasil.mp3?alt=media&token=none",duration=330*len(txt))
                line_bot_api.reply_message(event.reply_token, audio_message)   
        if text.lower().startswith("/搜圖"):
            if text.lower().replace("/搜圖","") == "":
                set_sauce = setting["sauce"]
                message = TextSendMessage(text="目前為:%s\n格式:/搜圖 {on/off}"%(set_sauce))
                line_bot_api.reply_message(event.reply_token, message)  
            if len(text.split(" ")) == 2:
                toggle = text.lower().split(" ")[1]
                if toggle == "on":
                    setting["sauce"] = True
                    msg = "搜圖已開啟\n搜圖會花一段時間，請耐心等待"
                if toggle == "off":
                    setting["sauce"] = False
                    msg = "搜圖已關閉"
                message = TextSendMessage(text=msg)
                line_bot_api.reply_message(event.reply_token, message) 
        if text.lower().startswith("/moe"):
            if text.lower().replace("/moe","") == "":
                set_moe = setting["moe"]
                message = TextSendMessage(text="目前為:%s\n格式:/moe {on/off}"%(set_moe))
                line_bot_api.reply_message(event.reply_token, message)  
            if len(text.split(" ")) == 2:
                toggle = text.lower().split(" ")[1]
                if toggle == "on":
                    setting["moe"] = True
                    msg = "moe搜圖已開啟\n搜圖會花一段時間，請耐心等待"
                if toggle == "off":
                    setting["moe"] = False
                    msg = "moe搜圖已關閉"
                message = TextSendMessage(text=msg)
                line_bot_api.reply_message(event.reply_token, message) 
    if isinstance(event.message, ImageMessage):
        if setting["sauce"] == True:
            message_content = line_bot_api.get_message_content(event.message.id)
            file_name = "temp" + '.jpg'
            # file_message = event.message.id + '.txt'
            with open(file_name, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            upload(file_name,file_name)
            url = "https://firebasestorage.googleapis.com/v0/b/fbclass-7e786.appspot.com/o/temp.jpg?alt=media&token=none"
            Ascii = ascii2d(url)
            msg = 'Ascii 搜尋結果\n'
            
            print(Ascii)
            for i in range(0,len(Ascii)):
                msg += Ascii[i] + '\n'
            Sauce = saucenao(url)
            msg += 'SauceNAO搜圖結果\n' + Sauce + '\n'
            message = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, message) 
            setting["sauce"] = False
        if setting["moe"] == True: 
            message_content = line_bot_api.get_message_content(event.message.id)
            file_name = "moe" + '.jpg'
            # file_message = event.message.id + '.txt'
            with open(file_name, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            moe_result = tracemoe.search('moe.jpg', encode=True)
            print(moe_result)
            docs = moe_result["docs"]
            docs_len = len(docs)
            title = []
            title_chinese = []
            msg = ""
            for i in range(0,docs_len):
                title.append(docs[i]["title"])
                title_chinese.append(docs[i]["title_chinese"])
            for j in range(0,len(title)):
                if j != 0:
                    if title[j] == title[j-1]:
                        pass
                    else:
                        msg += "日文片名:{}\n中文片名:{}\n\n".format(title[j],title_chinese[j])
                else:
                    msg += "日文片名:{}\n中文片名:{}\n\n".format(title[j],title_chinese[j])
            message = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, message)
            setting["moe"] = False



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
