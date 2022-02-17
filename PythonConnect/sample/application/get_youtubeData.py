import json
import collections
from socket import timeout
from googleapiclient.discovery import build
import urllib.parse
import unicodedata
import re
from . import KeyEnum 

class get_youtubeData:

    def __init__(self, API_KEY, YOUTUBE_API_SERVICE_NAME = 'youtube', YOUTUBE_API_VERSION = 'v3'):
        #動画検索
        self.API_KEY = API_KEY
        self.YOUTUBE_API_SERVICE_NAME = YOUTUBE_API_SERVICE_NAME
        self.YOUTUBE_API_VERSION = YOUTUBE_API_VERSION

        self.Key = KeyEnum.Key
        self.KeyNum = KeyEnum.KeyNum
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.API_KEY
        )
        self.VIDEO_ID_LIST = []
        #取得するデータは以下
        self.OUTPUT_TITLE = []
        self.OUTPUT_DESCRIPTION = []
        self.OUTPUT_TAGS = []
        self.OUTPUT_URL = []
        self.ALLDATA = []
        #-----for analyze------
        self.ANALYZE_TITLE = []
        self.ANALYZE_DESCRIPTION = []
        self.ANALYZE_TAGS = []
        self.ANALYZE_URL = []

        #-------------for output------------
        self.RATE_TITLE = []
        self.RATE_DESCRIPTION = []
        self.RATE_TAG = []

        #---------------点数計算用-----------------
        self.scoreRate = 25
        

    #Django側でajaxで関数を走らせる時、このインスタンスが作成されるタイミングは、ページに遷移した時、ボタンを押すときは遷移時にし生成したインスタンスの関数を叩いているので、ページ遷移が発生しない間は常に同じインスタンスを扱うことになる
   
    #例外処理を加えたKey取得
    def get_key(self, input_data, key):
        
        try:
            if key  == "url":
                getdata = input_data['snippet']['thumbnails']['high']['url']
            else:
                getdata = input_data['snippet'][key]
            return getdata
        except KeyError:
            print('KeyError No', key)

    #リストの平坦化
    def flatten_list(self, l):
        for el in l:
            if isinstance(el, list):
                yield from self.flatten_list(el)
            else:
                yield el
    #平坦化したデータを再びリストに変化する

    def set_data(self, input):
        return list(self.flatten_list(input))

    #要素の種類別にカウントが多い順に取得
    def count_data(self, input):
        output  = collections.Counter(self.set_data(input))
        return output

    def setKeyNum(self, Search_Key, MAX_RESULT):
        #検索したいキーワード
        self.Search_Key = Search_Key
        #取得した動画をリストに格納
        self.MAX_RESULT = MAX_RESULT

                #取得した動画をリストに格納
        id_list = []
        youtube_query = self.youtube.search(timeout = 2000).list(q=self.Search_Key, part='id,snippet', maxResults=self.MAX_RESULT)
        youtube_res = youtube_query.execute()
        result = youtube_res.get('items', [])
        # print("+++++++++++++++++++++++++++++++++++++++++++++\n")
        # print(result)
        # print("+++++++++++++++++++++++++++++++++++++++++++++\n")
        for item in result:
            if item['id']['kind'] == 'youtube#video':
                # print(item['snippet']['title'])
                # print('https://www.youtube.com/watch?v=' + item['id']['videoId'])
                id_list.append(item['id']['videoId'])

        VIDEO_ID_LIST = id_list

        for video_id in VIDEO_ID_LIST:
            response = self.youtube.videos().list(
            part = 'snippet,statistics',
            id = video_id
            ).execute()

            for item in response.get("items", []):
                if item["kind"] != "youtube#video":
                    continue
                self.OUTPUT_TITLE.append(self.get_key(item, self.Key.TITLE.value))
                self.OUTPUT_URL.append(self.get_key(item, self.Key.URL.value))
                self.OUTPUT_DESCRIPTION.append(self.get_key(item, self.Key.DESCRIPTION.value))
                self.OUTPUT_TAGS.append(self.get_key(item, self.Key.TAGS.value))
                
        self.ALLDATA.append(self.set_data(self.OUTPUT_TITLE))
        self.ALLDATA.append(self.set_data(self.OUTPUT_URL))
        self.ALLDATA.append(self.set_data(self.OUTPUT_DESCRIPTION))
        self.ALLDATA.append(self.count_data(self.OUTPUT_TAGS))

    def getdata(self,  data_key, TagNum = 0, UrlNum = 0, TagZip = True):
        data_key = int(data_key)
        if data_key == self.KeyNum.TAGS:
            if TagZip == True:
                return zip(*(self.ALLDATA[data_key].most_common(TagNum)))
                # return list(map(list, (zip(*self.ALLDATA[data_key].most_common(TagNum)))))
            else:
                return self.ALLDATA[data_key].most_common(TagNum)
        elif data_key == self.KeyNum.URL:
            return self.ALLDATA[data_key][0:UrlNum]
        else:
            return self.ALLDATA[data_key]

    def analyze_set(self, url_list):
        #---------------------動画IDのみURLから抽出---------------------------
        vid_list = []
        pattern_watch = 'https://www.youtube.com/watch?'
        pattern_short = 'https://youtu.be/'
        for i, url in enumerate(url_list):
            # 通常URLのとき
            if re.match(pattern_watch,url):
                yturl_qs = urllib.parse.urlparse(url).query
                vid = urllib.parse.parse_qs(yturl_qs)['v'][0]
                vid_list.append(vid)
            # 短縮URLのとき
            elif re.match(pattern_short,url):
                # "https://youtu.be/"に続く11文字が動画ID
                vid = url[17:28]
                vid_list.append(vid)
            else:
                print('error:\n  URLは\"https://www.youtube.com/watch?\"か')
                print('  \"https://youtu.be/\"で始まるURLを指定してください。')
                print('  - '+ str(i+1)+ '個目：' + url)
        
        response = self.youtube.videos().list(
        part = 'snippet,statistics',
        id = vid_list
        ).execute()
        #---------------------data save---------------------------
        for item in response.get("items", []):
            if item["kind"] != "youtube#video":
                continue
            self.ANALYZE_TITLE.append(self.get_key(item, self.Key.TITLE.value))
            self.ANALYZE_URL.append(self.get_key(item, self.Key.URL.value))
            self.ANALYZE_DESCRIPTION.append(self.get_key(item, self.Key.DESCRIPTION.value))
            self.ANALYZE_TAGS.append(self.get_key(item, self.Key.TAGS.value))
        # print("TITLE:{}".format(self.ANALYZE_TITLE))
        # print("DESCRIPTION:{}".format(self.ANALYZE_DESCRIPTION))
        # print("TAGS:{}".format(self.ANALYZE_TAGS))
        # print("IMAGE:{}".format(self.ANALYZE_URL))
                
    def analyze_do(self,  word):
        #------------------キーワードの出現位置の取得、割合の計算---------------------
        if len(self.ANALYZE_TITLE) > 0 and len(self.ANALYZE_DESCRIPTION) > 0:
            titleLen, titlePlace, titleRate = self.calc(self.ANALYZE_TITLE[0], word, KeyEnum.KeyNum.TITLE)
            desLen, desPlace, desRate = self.calc(self.ANALYZE_DESCRIPTION[0], word, KeyEnum.KeyNum.DESCRIPTION)
            self.RATE_TITLE = list((titleRate, titleLen, titlePlace))
            self.RATE_DESCRIPTION = list((desRate, desLen, desPlace))
            try:
                tagNum = len(self.ANALYZE_TAGS[0]) 
                # print("tagNum:".format(tagNum))
                #tagの文字数（スペース無視）
                sum = 0
                Place = 0   
                pt = 0
                # for tag in self.ANALYZE_TAGS[0]:
                if tagNum < 1:
                    print("NOTAG")
                else:
                    tagcnt = 0
                    for tag in self.ANALYZE_TAGS[0]:
                        sum += len(tag)
                        Place = 1 if self.findAllPos(tag, word) >= 0 else 0
                        if Place != 0 and tagcnt == 0:
                            pt = self.scoreRate
                        tagcnt += 1
                        
                    #     print(tag)
                    # print(sum)
                    self.RATE_TAG = list((pt, tagNum, sum))
            except TypeError:
                self.RATE_TAG = list((0, 0, 0))
        else:
            print("Ïndexerror")

    def getDataToDjango(self, key):
        if key == KeyEnum.KeyNum.TITLE:
            List = []
            for i in self.ANALYZE_TITLE:
                List.append(self.reshapetext(i))
            return List, self.RATE_TITLE

        elif key == KeyEnum.KeyNum.DESCRIPTION:
            List = []
            for i in self.ANALYZE_DESCRIPTION:
                List.append(self.reshapetext(i))
            return List, self.RATE_DESCRIPTION

        elif key == KeyEnum.KeyNum.TAGS:
            try:
                return self.ANALYZE_TAGS[0], self.RATE_TAG
            except TypeError:
                return [0], self.RATE_TAG

        elif key == KeyEnum.KeyNum.URL:
            try:
                return self.ANALYZE_URL, self.scoreRate
            except TypeError:
                return 0, 0



    @staticmethod
    def reshapetext(text):
        # tables = ['\u3000','　',' ','\x0c','\x0b','\t','\n','\r']
        tables = ['\u3000','\x0c','\x0b','\t','\n','\r']
        table = str.maketrans({
        v: '' for v in tables
        })
        text = text.translate(table)
        # text = ''.join(text.splitlines())
        # text = re.sub(r"\s", "", text)
        text = text.replace("\\"+"n","")
        # print(text)
        # print("------------------------------------------------------------------\n")
        return text

    @staticmethod
    def findAllPos(text, word):
        # textU = text.upper()
        word = word.lower()
        textL = text.lower()
        # PosU = textU.find(word)
        PosL = textL.find(word) 
        # print(word)
        # print(textL)
        # print("--------*******************************************************-----\n")
        # print(PosL)
        return PosL
        # if PosU > -1 or PosL > -1:
        #     rate = (abs(PosU)+1) / (abs(PosL)+1)
        #     if rate < 1:
        #         print(PosU)
        #         return PosU
        #     else:
        #         print(PosL)
        #         return PosL
        # elif PosU  == -1 and PosL == -1:
        #     print(-1)
        #     return -1


    def calc(self, text, word, key = -1):
        try:
            self.reshapetext(text)
            count = 0
            countNum = 0
            wordNum = 0
            maxWord = 0
            shortText = "sample"
            maxFlag = False
            if key == KeyEnum.KeyNum.TITLE:
                maxWord = 60
            elif key == KeyEnum.KeyNum.DESCRIPTION:
                maxWord = 200
            else:
                maxWord = 0

            for c in text:
                print(c)
                if unicodedata.east_asian_width(c) in 'FWA':
                    count += 1
                    countNum += 1
                    wordNum += 1
                elif c == " ":
                    countNum += 1
                    # print('CONTINUE')
                    continue
                # elif unicodedata.east_asian_width(c) in ["Na", "H", "N"]:
                else:    
                    count += 0.5
                    countNum += 1
                    wordNum += 1

                if  maxWord != 0 and count == maxWord:
                    maxFlag = True
                    shortText = text[0:countNum]
                if maxFlag == False:
                    shortText = text
                    
            print(shortText)
            print("------------------------------------------------------------------\n")
            Len = len(shortText)
            Place = self.findAllPos(shortText, word) if self.findAllPos(shortText, word) >= 0 else 0
            Rate = (1 - (Place/Len+0.0001))*self.scoreRate if Place != 0 else 0
            trueLen = wordNum
                    
            return trueLen, Place, Rate

        except IndexError:
            # raise
            print("url error")
            pass


    def urlCheck(self, url):
        #---------------------動画IDのみURLから抽出---------------------------
        pattern_watch = 'https://www.youtube.com/watch?'
        pattern_short = 'https://youtu.be/'
        # 通常URLのとき
        if re.match(pattern_watch,url):
            try:
                return True
            except KeyError:
                return False
        # 短縮URLのとき
        elif re.match(pattern_short,url):
            return True
        else:
            print('error:\n  URLは\"https://www.youtube.com/watch?\"か')
            print('  \"https://youtu.be/\"で始まるURLを指定してください。')
            return False