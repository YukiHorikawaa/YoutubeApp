from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# application/write_data.pyをインポートする
from .application import write_data
from .application import get_youtubeData
from .application.utils import get_json
from .application import KeyEnum

global output_dict


def SearchTAG(req):
    return render(req, 'SearchTAG.html')
    

# def ouput(req, output_dict):
#     return render(req, 'tagOutput.html', output_dict)

def call_write_word(req):
    print("get")
    print("TAG")
    searchNum = 50
    youtube = get_youtubeData.get_youtubeData('AIzaSyD_0S45BFbJ2Yo2nJmkxLteoxLZuES9Q9g')
    output_dict = {'title':'', 'url':'', 'tags':'', 'description':''}               
    if req.method == 'GET':
        # print(KeyEnum.Key.TAGS)
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        # write_data.write_csv(req.GET.get("input_data"))
        data = req.GET.get("input_word")
        print(data)
        #-----------------jsonでデータ取得、加工-----------------------
        jsonmanager = get_json.get_json(data)
        word = jsonmanager.getWord("word")
        # print(word)
        #-----------------指定URLに対して指定単語でデータ解析-----------------------
        youtube.setKeyNum(word,  searchNum)
        title = youtube.getdata(KeyEnum.KeyNum.TITLE)
        # print(title)
        print('---------------------------------------------------------------------------------')
        url = youtube.getdata(KeyEnum.KeyNum.URL, UrlNum=2)
        # print(url)
        print('---------------------------------------------------------------------------------')
        description = youtube.getdata(KeyEnum.KeyNum.DESCRIPTION)
        # print(description)
        print('---------------------------------------------------------------------------------')
        tags, Num = youtube.getdata(KeyEnum.KeyNum.TAGS, TagNum=50, TagZip = True)
        tags = list(tags)
        Num = list(Num)
        if tags[0] == None:
            tags = tags[1:len(tags)]
            Num = Num[1:len(Num)]
        print(tags)
        print("----------------------------num--------------------")
        print(Num)
        print('---------------------------------------------------------------------------------')
        #-----------------それぞれのデータ取得------------------------
        


        output_dict = {'title':title, 'url':url, 'tags':list(tags), 'description':list(description), 'tagNum':list(Num)}
        # print(output_dict)

        # return ouput(req, output_dict)
        # return SearchTAG(req)
        # return render(req, 'SearchTAG.html', output_dict)
        return JsonResponse(output_dict)
