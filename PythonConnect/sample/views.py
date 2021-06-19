from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# application/write_data.pyをインポートする
from .application import write_data
from .application import get_youtubeData
from .application.utils import get_json
from .application import KeyEnum


global url
global word

# Create your views here.
def index(req):
    return render(req, 'index.html')
def YoutubeSEO(req):
    return render(req, 'YoutubeSEO.html')

# ajaxでurl指定したメソッド
def call_write_data(req):
    youtube = get_youtubeData.get_youtubeData('AIzaSyD_0S45BFbJ2Yo2nJmkxLteoxLZuES9Q9g')
    print("get")
    print("SEO")
    if req.method == 'GET':
        # print(KeyEnum.Key.TAGS)
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        # write_data.write_csv(req.GET.get("input_data"))
        data = req.GET.get("input_data")
        print(data)
        #-----------------jsonでデータ取得、加工-----------------------
        jsonmanager = get_json.get_json(data)
        url = jsonmanager.getUrl("url")
        word = jsonmanager.getWord("word")
        if url == "":
            output_dict = {'error': int(0), 'string':str("Please fill in the URL.")}
            print("urlが設定できていません:{}".format(output_dict))
            return JsonResponse(output_dict)
        elif word == "":
            output_dict = {'error': int(1), 'string':str("Please fill in the Keyword.")}
            print("wordが設定できていません:{}".format(output_dict))
            return JsonResponse(output_dict)
        else:
            if youtube.urlCheck(url):
                print(url)
                print(word)
                try:
                    #-----------------指定URLに対して指定単語でデータ解析-----------------------
                    youtube.analyze_set([url])
                    youtube.analyze_do(word)
                    #-----------------それぞれのデータ取得------------------------
                    title, titleRate = youtube.getDataToDjango(KeyEnum.KeyNum.TITLE)
                    description, descriptionRate = youtube.getDataToDjango(KeyEnum.KeyNum.DESCRIPTION)
                    tags, tagRate = youtube.getDataToDjango(KeyEnum.KeyNum.TAGS)
                    url, urlScore= youtube.getDataToDjango(KeyEnum.KeyNum.URL)
                    TotalScore = titleRate[0] + descriptionRate[0] + tagRate[0] + urlScore
                except IndexError:
                    output_dict = {'error': int(2), 'string':str("Probably a misspelling.")}
                    print("おそらくタイプミス:{}".format(output_dict))
                    return JsonResponse(output_dict)
                except KeyError: 
                    output_dict = {'error': int(2), 'string':str("Probably a misspelling.")}
                    print("おそらくタイプミス:{}".format(output_dict))
                    return JsonResponse(output_dict)
                except ValueError:
                    output_dict = {'error': int(2), 'string':str("Probably a misspelling.")}
                    print("おそらくタイプミス:{}".format(output_dict))
                    return JsonResponse(output_dict)
                except UnboundLocalError: 
                    output_dict = {'error': int(2), 'string':str("Probably a misspelling.")}
                    print("おそらくタイプミス:{}".format(output_dict))
                    return JsonResponse(output_dict)
                # print("TAGS:{} len:{}".format(youtube.ANALYZE_TAGS[0], len(youtube.ANALYZE_TAGS[0])))
                print("title:{}\n description:{}\n tag:{}".format(titleRate, descriptionRate, tagRate))
                
                # output_dict = {'title':str(title), 'titleRate':str(titleRate), 'description':str(description), 'descriptionRate':str(descriptionRate), 'tags':str(tags), 'tagRate':str(tagRate)}
                output_dict = {'title':title, 'titleRate':titleRate, 'description':description, 'descriptionRate':descriptionRate,'tags':tags,'tagRate':tagRate,'urlScore':urlScore,'url':url, 'TotalScore':TotalScore, 'string':str("Successfully analyzed.")}

                print(output_dict)
                return JsonResponse(output_dict)
            else:
                output_dict = {'error': int(2), 'string':str("Please enter a valid URL.")}
                print("URLリンク先がありません:{}".format(output_dict))
                return JsonResponse(output_dict)


def errorHandler(errNum, errString):
    output_dict = {'error': int(errNum), 'string':str(errString)}
    print("おそらくタイプミス:{}".format(output_dict))
    return JsonResponse(output_dict)