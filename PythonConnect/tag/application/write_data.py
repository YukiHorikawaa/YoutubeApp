# coding:utf-8
import os
import csv
from . import get_youtubeData
from. import KeyEnum 

youtube = get_youtubeData.get_youtubeData('AIzaSyD_0S45BFbJ2Yo2nJmkxLteoxLZuES9Q9g')

# htmlからのデータをcsvファイルに記録
def write_csv(data):
    datas = [data]
    youtube.setKeyNum(datas,  50)
    output = youtube.getdata(KeyEnum.KeyNum.TAGS, TagNum=20, TagZip = False)
    print(output)
    # youtube.analyze_do("こち亀")
    with open(os.getcwd()+'/sample/application/'+'data.csv','a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(output)