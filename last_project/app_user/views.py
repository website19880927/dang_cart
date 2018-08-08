import os
import random
import string

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from app_user.captcha.image import ImageCaptcha
from main.models import User, MyString


def login_page(request):
    #用户名或者密码错误显示

    error= request.session.get('error')
    if not error:
        error=''
    else:
        del request.session['error']
    re = {'error':error}
    #从订单页面传过来的登录，标志，如果登录成功直接跳转到地址页面。

    if request.GET.get('flag'):
        print('进入登录，fromcart')
        request.session['from_cart']=request.GET.get('flag')


    return render(request,'user/login.html',re)

def login_logic(request):

    u=request.POST.get('username')
    p=request.POST.get('password')
    c=request.POST.get('code')
    print(u, c, request.session.get('code'))
    if request.session.get('code')==c:
        if User.objects.filter(username=u) and User.objects.filter(password=p):
            request.session['name']=u
            if request.session.get('from_cart'):
                print('from cart 登录后回去了')
                re=redirect('order:address')
            else:
                re=redirect('main:all')
            if request.POST.get('autologin'):
                #设置cookie
                re.set_cookie('password',p,max_age=7*24*3600)
                return re
            else:
                return re
    else:
        request.session['error']='输入错误请检查用户名与密码'
        return redirect('user:login')


def ajax(request):
    n=request.POST.get('username')
    print(n)
    print(request.POST.get('code'))

    #异步判断用户名是否存在 如果存在 就返回用户名存在，改名字
    if User.objects.filter(username=n):
        return HttpResponse('用户名合法')
    #异步取得验证码，如果与之前存的验证码相同 就返回
    elif request.POST.get('code'):

        if request.POST.get('code')==request.session['code']:
            return  HttpResponse('正确')
        else:
            return HttpResponse('不正确')
    else:
        return HttpResponse('用户名不存在,请注册')

def regist(request):

    return render(request,'user/register.html')

def regist_logic(request):
    u=request.POST.get('username')
    p=request.POST.get('password')

    try:
        with transaction.atomic():
            User.objects.create(username=u,password=p)
            request.session['name']=u
            return render(request,'user/register ok.html',{'name':u})
    except:
        return redirect('user:regist')
def capta(request):
    img = ImageCaptcha(fonts=[os.path.abspath('font/simsun.ttc')])
    print(img,os.path.abspath('font/segoesc.ttf'))
    # 产生图片对象
    # code = random.sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 2)
    code = random.sample(MyString.digits+MyString.han, 4)
    # 将列表转换字符串
    request.session['code']=code
    print(code)
    code_string = ''.join(code)
    request.session['code'] = code_string
    image = img.generate(code_string)
    print(image,type(image))
    return HttpResponse(image, 'img/png')

def test(request):

    # return render(request,'user/register ok.html')
    request.session['pd']=1

    return render(request,'main/test.html')