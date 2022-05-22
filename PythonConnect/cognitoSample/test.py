import jwt

# id_token = "eyJraWQiOiI5amtvc2tGZWlnOHA1aDJRQkVGdUl3WE5xVGJDZXdTczFEV1VzZHRDdkNNPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicUljbE1KM29vdmh0ZmFpLW1EQkg0USIsInN1YiI6IjVkNDAyMjUyLTE3NjAtNDBhYy05ZDdkLWYwZmFjNTc3NTA4NCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtbm9ydGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtbm9ydGhlYXN0LTFfM3JkUjROSmRrIiwiY29nbml0bzp1c2VybmFtZSI6IjVkNDAyMjUyLTE3NjAtNDBhYy05ZDdkLWYwZmFjNTc3NTA4NCIsImF1ZCI6IjVhbmk0cW1zdjJtaWpqY2pnOWFmMjQ4bHE4IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NTMyMTA1NzgsIm5hbWUiOiJZdWtpIiwiZXhwIjoxNjUzMjk2OTc4LCJpYXQiOjE2NTMyMTA1NzgsImp0aSI6IjAxMDUzMjJiLWQxZTctNDAyYy1iMWEyLTNkOTkyNGU4NDU5MCIsImVtYWlsIjoibWFuZG9yaW55dWtpQGljbG91ZC5jb20ifQ.KylAwg0U7WN7PjK_MxUqxvzqwMkPOpB_SbsK5DjaNkYjk7Wq8UP71Szri90FLKg6hZl9_q8J6C6xVWNTJxLPXnJv3NpkM_dv0MLTIqN2NdNVKzfdml39nuPQPYZhOYU2ea3JCJKQh0S6cmyZZNBgc5SQHnjszdaA_U_cLZyvOMyLf90MCSoQ36kw2GPVaFJVwx_HJuoAVavPrJiOUvZu0URfFjI2MjKpk3EIpxrKu_5p52FUrfEUQgzNEOerSMXjSBCEyQQjXH3j1bglNMt8oV3lnNsN3OxS_lhsulAhqBR897t5NATWOgNPnHhW_liQu7hkNpxDVCSbyx4wDTRcqQ"

# # まずは中身を見る。
# decoded_header = jwt.get_unverified_header(id_token)
# decoded_payload = jwt.decode(id_token, options={"verify_signature": False})

# print(decoded_header,decoded_payload)


import requests
from jwt.algorithms import RSAAlgorithm
import json
import base64
import os
# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv()

# 公開してはいけません( ;∀;)
token_from_cognito = "eyJraWQiOiI5amtvc2tGZWlnOHA1aDJRQkVGdUl3WE5xVGJDZXdTczFEV1VzZHRDdkNNPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoicUljbE1KM29vdmh0ZmFpLW1EQkg0USIsInN1YiI6IjVkNDAyMjUyLTE3NjAtNDBhYy05ZDdkLWYwZmFjNTc3NTA4NCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtbm9ydGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtbm9ydGhlYXN0LTFfM3JkUjROSmRrIiwiY29nbml0bzp1c2VybmFtZSI6IjVkNDAyMjUyLTE3NjAtNDBhYy05ZDdkLWYwZmFjNTc3NTA4NCIsImF1ZCI6IjVhbmk0cW1zdjJtaWpqY2pnOWFmMjQ4bHE4IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NTMyMTA1NzgsIm5hbWUiOiJZdWtpIiwiZXhwIjoxNjUzMjk2OTc4LCJpYXQiOjE2NTMyMTA1NzgsImp0aSI6IjAxMDUzMjJiLWQxZTctNDAyYy1iMWEyLTNkOTkyNGU4NDU5MCIsImVtYWlsIjoibWFuZG9yaW55dWtpQGljbG91ZC5jb20ifQ.KylAwg0U7WN7PjK_MxUqxvzqwMkPOpB_SbsK5DjaNkYjk7Wq8UP71Szri90FLKg6hZl9_q8J6C6xVWNTJxLPXnJv3NpkM_dv0MLTIqN2NdNVKzfdml39nuPQPYZhOYU2ea3JCJKQh0S6cmyZZNBgc5SQHnjszdaA_U_cLZyvOMyLf90MCSoQ36kw2GPVaFJVwx_HJuoAVavPrJiOUvZu0URfFjI2MjKpk3EIpxrKu_5p52FUrfEUQgzNEOerSMXjSBCEyQQjXH3j1bglNMt8oV3lnNsN3OxS_lhsulAhqBR897t5NATWOgNPnHhW_liQu7hkNpxDVCSbyx4wDTRcqQ"


def is_valid(token_from_cognito):
    # ここは各自の変数
    cognito_user_pool_id = "ap-northeast-1_3rdR4NJdk" # 変える
    cognito_app_client_id = "5ani4qmsv2mijjcjg9af248lq8" # 変える
    aws_region = "ap-northeast-1"

    # ここからは共通
    cognito_iss = "https://cognito-idp."+ aws_region +".amazonaws.com/" + cognito_user_pool_id
    cognito_jwk_url = cognito_iss + '/.well-known/jwks.json'
    jwk_set = requests.get(cognito_jwk_url).json()

    header = jwt.get_unverified_header(token_from_cognito)
    jwk = next(filter(lambda x: x['kid'] == header['kid'], jwk_set['keys']))
    public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

    try:
        claims = jwt.decode(
                    token_from_cognito,
                    public_key,
                    issuer=cognito_iss,
                    audience=cognito_app_client_id,
                    algorithms=jwk['alg'],
        )
        print("claimsの中身→",claims)

        print('ユーザーのemail',claims["email"])

        if claims['aud'] != cognito_app_client_id:
            return False
        if claims['iss'] != cognito_iss:
            return False
        if claims['token_use'] != "id":
            return False
        return True
    except Exception as e:
        # だいたい期限切れのエラー
        print("トークンの検証失敗：原因→",str(e))
        return False
        

is_valid(token_from_cognito)
print("///////////////////////////////////////")



# # Create your views here.
# def index(request): 
#     context = {}
#     try:
#         code = request.GET.get("code")
#         userData = getTokens(code)
#         context['name'] = userData['name']
#         context['status'] = 1

#         response = render(request, 'inded.html', context)
#         response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60*24, httponly=True)
#         return response
#         # return render(req, 'index.html', context)
#     except:
#         token = getSession(request)
#         if token is not None:
#             userData = decode_jwt.lambda_handler(token, None)
#             context['name'] = userData['name']
#             context['status'] = 1
#             return render(request, 'indexlhtml', context)
#         return render(request, 'indexlhtml', {'status':0})


def getTokens(code):
    TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")    
    print("TOKEN_ENDPOINT:{}".format(TOKEN_ENDPOINT))
    REDIRECT_URI = os.getenv("REDIRECT_URI")    
    print("REDIRECT_URI:{}".format(REDIRECT_URI))
    CLIENT_ID = os.getenv("CLIENT_ID")    
    print("CLIENT_ID:{}".format(CLIENT_ID))
    CLIENT_SCECRET = os.getenv("CLIENT_SCECRET")    
    print("CLIENT_SCECRET:{}".format(CLIENT_SCECRET))

    # ori = "djc98u3jiedmi283eu928:abcdef01234567890"
    ori = f"{CLIENT_ID}:{CLIENT_SCECRET}"

    # endcodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SCECRET}", "ISO-8859-1")).decode("ascii")
    endcodeData = base64.b64encode(ori.encode()).decode()
    endcodeData = "'"+endcodeData+"'"
    print("endcodeData:{}".format(endcodeData))
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        # "Content-Type" : "AWSCognitoIdentityProviderService.InitiateAuth",        
        "Authorization" : endcodeData
    }

    # body = {
    #     # "grant_type" : "authorization_code",
    #     "grant_type" : "lient_credentials",        
    #     # "scope" : "openid",
    #     "client_id" : CLIENT_ID,
    #     # 'code' : code,
    #     # 'redirect_uri' : REDIRECT_URI
    # }

    body = {
        "grant_type" : "authorization_code",
        "client_secret" : CLIENT_SCECRET,        
        "scope" : "openid",
        "client_id" : CLIENT_ID,
        'code' : code,
        'redirect_uri' : REDIRECT_URI
    }

    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers)
    print("response:{}".format(response))
    print("response.json():{}".format(response.json()))

    id_token = response.json()['id_token']
    print("id_token:{}".format(id_token))

    userData = decode_jwt.lambda_handler(id_token, None)
    print("userData:{}".format(userData))

    if not userData:
        return False
    
    user = {
        'id_token' : id_token,
        'name' : userData['name'],
        'email' : userData['email'],
    }
    return user

inputdata = "37ea8616-ade1-47b0-977a-31327691e065"

print(getTokens(inputdata))

# def getSession(request):
#     try:
#         response = request.COOKIES['sessiontoken']
#         return response
#     except:
#         return None

    # response = {
    #     id_token : 'abc',
    #     access_token : 'aaa',
    #     refresh_token : 'aaa'
    # }

