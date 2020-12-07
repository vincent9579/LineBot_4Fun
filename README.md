# `LineBot4Fun` 一個好用的Line機器人

加好友  ➤  [Link button](https://line.me/R/ti/p/%40175odroc)

[LineBot_4Fun](https://github.com/vincent9579/LineBot_4Fun)，是一款基於`Python`的LineBot

在現在這個忙碌的世界，很多事情都是交給AI或是機器人處理，但卻沒有一個機器人是完美的。難道沒辦法用一隻機器人，就能處理好所有的雜事嗎？這機器人就是基於這樣的理念創作出來的，在短時間內、在我能力所及之下拼拼湊湊出來的。





---

## 安裝

### ➤ 在開始前請先將所有Token及所需API Config更換掉

#### 安裝需要python 3.6以上

下載專案後，解壓縮

在跟專案的同層目錄中 開啟CMD

輸入

`$ pip3 install -r requirements.txt`

安裝所有所需套件

接下來在伺服器中執行檔案即可

`$ python3 app.py`



記得[Line開發者平台](https://developers.line.biz/console/)中的Webhook網址要改成你自己伺服器的網址

## 功能

### 完整的功能列表
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/Help.png?raw=true)

### 天氣查詢 (使用中央氣象局API)
#### 格式：`天氣 縣市名稱`

### 字典(使用[zdict](https://github.com/zdict/zdict))
#### 格式：`/字典 查詢字典 字詞`

字典支持以下幾種 ：

Yahoo Dictionary

Moe Dictionary 萌典

Urban Dictionary

SpanishDict

Jisho Japanese Dictionary

Yandex Translate

Oxford Dictionary

Wiktionary

iTaigi-愛台語

國家教育研究院 - 雙語詞彙、學術名詞暨辭書資訊網

原住民族語言線上詞典



![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/Dict.jpg?raw=true)

### 文字轉語音(使用gTTs)
#### 格式：`/語音_語言_字詞`
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/gtts.jpg?raw=true)

### 繁體/簡體轉換(使用繁化姬API)
#### 格式：`/繁化_模式_字詞`

模式支援以下幾種

Simplified （簡體化）

Traditional （繁體化）

China （中國化）

Hongkong （香港化）

Taiwan （台灣化）

Pinyin （拼音化） 

Bopomofo （注音化）

Mars （火星化）

WikiSimplified （維基簡體化）

WikiTraditional （維基繁體化）




![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/zhconvert1.jpg?raw=true)
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/zhconvert2.jpg?raw=true)

### 新冠病毒即時資訊(使用disease.sh的API)
#### 格式：`/covid 國家`
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/covid.jpg?raw=true)

### 動畫搜圖-用一張圖片找動漫(使用[tracemoepy](https://github.com/DragSama/tracemoepy))
#### 使用`/moe on`開啟圖搜功能，搜尋需要十來秒不等。
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/moe.jpg?raw=true)

### 油圖搜索(爬[Ascii2D](https://ascii2d.net/)及[SauceNAO](https://saucenao.com/))
#### 使用`/搜圖 on`開啟圖搜功能，搜尋需要十來秒不等。
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/image_search.jpg?raw=true)

### 新聞內容擷取(使用[GeneralNewsExtractor](https://github.com/kingname/GeneralNewsExtractor))
#### 可以使用`/lockurl`或`/unlockurl`來選擇要不要開放擷取所有連結
![](https://github.com/vincent9579/LineBot_4Fun/blob/main/Example_img/news.jpg?raw=true)


---

## 使用套件
* [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
* [flask](https://palletsprojects.com/p/flask/)
* [requests](https://requests.readthedocs.io/en/master/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [zdict](https://github.com/zdict/zdict)
* [gne](https://github.com/kingname/GeneralNewsExtractor)
* [gTTS](https://github.com/pndurette/gTTS)
* [PyImgur](https://github.com/Damgaard/PyImgur)
* [tracemoepy](https://github.com/DragSama/tracemoepy)
* [pyrebase](https://github.com/nhorvath/Pyrebase4)

---