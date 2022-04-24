from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
# application/write_data.pyをインポートする
from .application import write_data
from .application import get_youtubeData
from .application.utils import get_json
from .application import KeyEnum
import json

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
        try:
            encoded = json.dumps(output_dict)
            print(HttpResponse)
            return HttpResponse(encoded, content_type = "application/json")
        except:
            print(JsonResponse)
            response = JsonResponse(output_dict)
            response['Access-Control-Allow-Origin'] = 'http://163.43.87.213:8000'
            #response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            return response


from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    title_name = u"djangoを使ったPostと値の取得テスト"
    content1 = """
    以下に名前を入力してください
    """
    content_dict = {"Title" : title_name,"content1" : content1}
    try:
        content_dict["name"] = request.POST.get('name', None)
    except:
        print("error")
    return render(request, 'direct/index.html', content_dict)


def no_url(request):    
    output_dict = {'title':'', 'url':'', 'tags':'', 'description':''}      
    #POSTリクエストがあった時  
    if request.method == 'POST':
        print("get")
        print("TAG")
        searchNum = 50
        youtube = get_youtubeData.get_youtubeData('AIzaSyDWn4f1TaQ6IwcSZBTv89a53O9FpU-xaJ8')   
        # print(KeyEnum.Key.TAGS)
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        # write_data.write_csv(request.GET.get("input_data"))
        word = request.POST.get('input_word', None)
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
        popFlag = False
        for i in range(len(tags)):
            if tags[i] == None:
                pop_num = i
                popFlag = True
        if popFlag:
            tags.pop(pop_num)
        print(tags)
        print("----------------------------num--------------------")
        print(Num)
        print('---------------------------------------------------------------------------------')
        #-----------------それぞれのデータ取得------------------------
        
        output_dict = {'title':title, 'url':url, 'tags':list(tags), 'description':list(description), 'tagNum':list(Num), 'input_word':str(word)}
        # output_dict = json.dumps(output_dict)
        # return render(request, 'direct/no_url_SearchTAG_out.html', {"data":output_dict})
        return render(request, 'direct/no_url_SearchTAG_out.html', output_dict)
        # try:
        #     return render(request, 'direct/no_url_SearchTAG.html', output_dict)
        # except:
        #     print(JsonResponse)
        #     response = JsonResponse(output_dict)
        #     response['Access-Control-Allow-Origin'] = 'http://163.43.87.213:8000'
        #     #response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'
            # return response

    else:
        print("normal")
        return render(request, 'direct/no_url_SearchTAG.html', output_dict)

