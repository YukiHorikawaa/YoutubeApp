from contextvars import Context
from email import header
from lib2to3.pgen2 import token
from urllib.error import ContentTooShortError
from django.shortcuts import render
from django.http import HttpResponse, response
from django.http import JsonResponse
from django.template import context
# from httpcore import request
# application/write_data.pyをインポートする
from .application import write_data
from .application import get_youtubeData
from .application.utils import get_json
from .application import KeyEnum
#for cognito
# from decouple import config
import base64
import requests
# from general import decode_jwt
# import decode_jwt



#--------------------cognito------------------
# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

from distutils.command.config import config
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

region = config('COGNITO_REGION_NAME')
userpool_id = config('USER_POOL_ID')
app_client_id = config('CLIENT_ID')
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']

def lambda_handler(token, context):
    # token = event['token']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    # print(claims)
    return claims
        

global url
global word

# Create your views here.
def index(request): 
    context = {}
    try:
        code = request.GET.get("code")
        userData = getTokens(code)
        context['name'] = userData['name']
        context['status'] = 1

        response = render(request, 'inded.html', context)
        response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60*24, httponly=True)
        return response
        # return render(req, 'index.html', context)
    except:
        token = getSession(request)
        if token is not None:
            userData = decode_jwt.lambda_handler(token, None)
            context['name'] = userData['name']
            context['status'] = 1
            return render(request, 'indexlhtml', context)
        return render(request, 'indexlhtml', {'status':0})


def getTokens(code):
    TOKEN_ENDPOINT = config("TOKEN_ENDPOINT")
    REDIRECT_URI = config("REDIRECT_URI")
    CLIENT_ID = config("CLIENT_ID")
    CLIENT_SCECRET = config("CLIENT_SCECRET")

    endcodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SCECRET}", "ISO-8859-1")).decode("ascii")

    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : f"Basic {endcodeData}"
    }

    body = {
        "grant_type" : "authorization_code",
        "client_id" : CLIENT_ID,
        'code' : code,
        'redirect_uri' : REDIRECT_URI
    }

    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers)

    id_token = response.json()['id_token']

    userData = decode_jwt.lambda_handler(id_token, None)

    if not userData:
        return False
    
    user = {
        'id_token' : id_token,
        'name' : userData['name'],
        'email' : userData['email'],
    }
    return user

def getSession(request):
    try:
        response = request.COOKIES['sessiontoken']
        return response
    except:
        return None

    # response = {
    #     id_token : 'abc',
    #     access_token : 'aaa',
    #     refresh_token : 'aaa'
    # }


def YoutubeSEO(req):
    return render(req, 'YoutubeSEO.html')
def Terms_service(req):
    return render(req, 'Terms_service.html')
# ajaxでurl指定したメソッド
def call_write_data(req):
    youtube = get_youtubeData.get_youtubeData('AIzaSyDWn4f1TaQ6IwcSZBTv89a53O9FpU-xaJ8')
    print("get")
    print("SEO")
    if req.method == 'GET':
        # print(KeyEnum.Key.TAGS)
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        # write_data.write_csv(req.GET.get("input_data"))
        data = req.GET.get("input_data")
        # print(data)
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
                    TotalScore = round(titleRate[0] + descriptionRate[0] + tagRate[0])
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



def no_url(request):
    youtube = get_youtubeData.get_youtubeData('AIzaSyDWn4f1TaQ6IwcSZBTv89a53O9FpU-xaJ8')
    print("get")
    print("SEO")
    if request.method == 'POST':
        # print(KeyEnum.Key.TAGS)
        # write_data.pyのwrite_csv()メソッドを呼び出す。
        # ajaxで送信したデータのうち"input_data"を指定して取得する。
        # write_data.write_csv(request.GET.get("input_data"))
        url = request.POST.get("url", None)
        word = request.POST.get("word", None)
        # if url == "":
        #     output_dict = {'error': int(0), 'string':str("Please fill in the URL.")}
        #     print("urlが設定できていません:{}".format(output_dict))
        #     return render(request, 'direct/index.html', output_dict)
        # elif word == "":
        #     output_dict = {'error': int(1), 'string':str("Please fill in the Keyword.")}
        #     print("wordが設定できていません:{}".format(output_dict))
        #     return render(request, 'direct/index.html', output_dict)
        # else:
        if youtube.urlCheck(url):
            print(url)
            print(word)
            #-----------------指定URLに対して指定単語でデータ解析-----------------------
            youtube.analyze_set([url])
            youtube.analyze_do(word)
            #-----------------それぞれのデータ取得------------------------
            title, titleRate = youtube.getDataToDjango(KeyEnum.KeyNum.TITLE)
            description, descriptionRate = youtube.getDataToDjango(KeyEnum.KeyNum.DESCRIPTION)
            tags, tagRate = youtube.getDataToDjango(KeyEnum.KeyNum.TAGS)
            url, urlScore= youtube.getDataToDjango(KeyEnum.KeyNum.URL)
            TotalScore = round(titleRate[0] + descriptionRate[0] + tagRate[0])

        # print("TAGS:{} len:{}".format(youtube.ANALYZE_TAGS[0], len(youtube.ANALYZE_TAGS[0])))
        print("title:{}\n description:{}\n tag:{}".format(titleRate, descriptionRate, tagRate))
        
        # output_dict = {'title':str(title), 'titleRate':str(titleRate), 'description':str(description), 'descriptionRate':str(descriptionRate), 'tags':str(tags), 'tagRate':str(tagRate)}
        output_dict = {'title':title, 'titleRate':titleRate, 'description':description, 'descriptionRate':descriptionRate,'tags':tags,'tagRate':tagRate,'urlScore':urlScore,'url':url, 'TotalScore':TotalScore, 'string':str("Successfully analyzed."), 'input_word':str(word)}

        print(output_dict)
        return render(request, 'direct/no_url_YoutubeSEO_out.html', output_dict)
    else:
        print("normal")
        return render(request, 'direct/no_url_YoutubeSEO.html')

