from email.header import Header
from django.shortcuts import render
from config.settings import KAKAO_CONFIG
from django.shortcuts import redirect
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def Login_view(request):
    CLIENT_ID = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = KAKAO_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRET_URL)
    res = redirect(url)
    return res

@api_view(['GET'])
def UserInfo_view(request):
    CODE = request.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
        'grant_type': 'authorization_code',
        'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
        'redirect_url': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
        'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
        'code': CODE
    }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    token_json = response.json()

    user_url = "https://kapi.kakao.com/v2/user/me"
    access_token =  token_json['access_token']
    auth = "Bearer " + token_json['access_token']

    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(user_url, headers=HEADER)
    json_data = res.json()
    user_id = json_data["id"]
    email = json_data["kakao_account"]["email"]

    if User.objects.filter(username = user_id).exists():
        user = User.objects.get(username = user_id)
    else:
        user = User.objects.create_user(
            username = user_id,
            first_name = email,
        )
        user.set_unusable_password()

    login_res = {
        'id' : user.id,
        'user_id' : user_id,
        'email' : email,
        'access_token': access_token,
    }
    login(request,user=user)
    return Response(login_res)

@login_required
def Logout_view(request):
    # kakao_admin_key = KAKAO_CONFIG['KAKAO_ADMIN_KEY']
    # logout_url = "https://kapi.kakao.com/v1/user/logout"
    # target_id = request.user.username
    # target_id = int(target_id)
    # HEADER = {
    #     "Authorization": f"KakaoAK {kakao_admin_key}"
    #     }
    # DATA = {
    #     "target_id_type": "user_id", 
    #     "target_id": target_id
    #     }
    # logout_res = requests.post(
    #     logout_url, headers=HEADER, data=DATA
    # ).json()
    # logout(request)
    # print('-----------------------------------------------------------------')
    # print(logout_res)
    # print('-----------------------------------------------------------------')
    # return redirect('home')
    logout(request)
    KAKAO_REST_API_KEY = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    KAKAO_LOGOUT_REDIRECT_URI = KAKAO_CONFIG['KAKAO_LOGOUT_REDIRECT_URI']
    state = "none"
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
    return redirect(
        f"{kakao_service_logout_url}?client_id={KAKAO_REST_API_KEY}&logout_redirect_uri={KAKAO_LOGOUT_REDIRECT_URI}&state={state}"
    )