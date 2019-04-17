# _*_ coding: utf-8 _*_
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
import re
from login.models import user
from login.md5 import md5_key
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def login(request):
    if request.session.get('is_login', None) != None:
        return redirect('/login/tables')
    return render(request, 'login/login.html')

def register(request):
    if request.session.get('is_login', None) != None:
        return redirect('/login/tables')
    return render(request, 'login/regist.html')

@csrf_exempt
def check(request):
    dealtype = request.POST.get("deal_type")
    dealval = request.POST.get("deal_val")
    message=''
    if dealtype == 'umail':
        try:
            lookfor = user.objects.get(umail=dealval)
            if lookfor:
                message = '邮箱已经被注册'
        except:
            message = ''
    if dealtype == 'uphone':
        try:
            lookfor = user.objects.get(uphone=dealval)
            if lookfor:
                message = '手机号已经被注册'
        except:
            message = ''
    ret = {'message':message}
    return JsonResponse(ret)

@csrf_exempt
def regist(request):
    if request.session.get('is_login', None) != None:
        return redirect('/login/tables')
    username = request.POST.get('username', None)
    password = request.POST.get('upassword', None)
    ufnamech = request.POST.get('ufnamech', None)
    ulnamech = request.POST.get('ulnamech', None)
    ufnameen = request.POST.get('ufnameen', None)
    ulnameen = request.POST.get('ulnameen', None)
    umail = request.POST.get('umail', None)
    uphone = request.POST.get('uphone', None)
    unamech = ufnamech+ulnamech
    unameen = ulnameen+ufnameen
    if password != None:
        password = md5_key(password)
    if not (username and password and umail and unameen and uphone):
        message = {'flag':'badmess','info':'您的信息有误，请检查'}
        return JsonResponse(message)
    else:
        us = user.objects.filter(uaccount = username)
        if us:
            message = {'flag':'badmess','info':'用户名重复'}
            return JsonResponse(message)
        mail = user.objects.filter(umail = umail)
        if mail:
            message = {'flag':'badmess','info':'邮箱重复'}
            return JsonResponse(message)
        phone = user.objects.filter(uphone = uphone)
        if phone:
            message = {'flag':'badmess','info':'手机重复'}
            return JsonResponse(message)
        new_test = user(uaccount=username, unamech = unamech, unameen = unameen, umail = umail,upassword=password, uphone = uphone, uall = False)
        new_test.save()
        message={'flag':'goodmess','info':'注册成功'}
        return JsonResponse(message)

def passway(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if password != None:
            password = md5_key(password)
        ret = re.match(r"^1[35678]\d{9}$", username)
        if not ret:
            try:
                usr = user.objects.get(umail = username)
                if usr.upassword == password:
                    request.session['is_login'] = True
                    request.session['username'] = usr.uaccount
                    request.session['usermail'] = usr.umail
                    if usr.unamech == '':
                        request.session['name'] = usr.unameen
                    else:
                        request.session['name'] = usr.unamech
                    request.session['uall'] = usr.uall
                    request.session.set_expiry(60*60)
                    return redirect('/login/tables')
                else:
                    message = '用户名或密码错误'
            except:
                message = '用户名或密码错误'
                return render(request, 'login/login.html', {"message": message})
        else:
            try:
                uph = user.objects.get(uphone = username)
                if uph.upassword == password:
                    request.session['is_login'] = True
                    request.session['username'] = uph.uaccount
                    request.session['usermail'] = uph.umail
                    if uph.unamech == '':
                        request.session['name'] = uph.unameen
                    else:
                        request.session['name'] = uph.unamech
                    request.session['uall'] = uph.uall
                    request.session.set_expiry(60*60)
                    return redirect('/login/tables')
                else:
                    message = '用户名或密码错误'
            except:
                message = '用户名或密码错误'
        return render(request, 'login/login.html', {"message": message})
        

def tables(request):
    if request.session.get('is_login', None) == None:
        return redirect('/login')
    else:
        return render(request, 'login/tables.html')

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/tables")
    request.session.flush()
    return redirect('/login/')

        