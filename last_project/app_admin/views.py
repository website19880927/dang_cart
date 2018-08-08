import datetime
import random
import string
from urllib import parse
from http import client
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from main.models import User, Category, Book, Address, Order


def index(request):
    #登录成功，获取name
    name=request.session.get('admin')

    return  render(request,'admin/index1.html',{'name':name})
def add(request):
    #获取第一类所有目录展示给用户，让其选择
    cate=Category.objects.filter(parent_id=1)
    print(cate)
    return  render(request,'admin/add.html',{'cate':cate})
def ajax_add(request):
    name=request.GET.get('change')
    id=Category.objects.filter(title=name)[0].id
    print(id)
    title=list(Category.objects.filter(parent_id=id).values())
    return  JsonResponse(title,safe=False)
def add_logic(request):
    n1=request.POST.get('name')
    n2=request.POST.get('author')
    n3=request.FILES.get('cover')
    n4=request.POST.get('market_price')
    n5=request.POST.get('dang_price')
    n6=request.POST.get('sales_amount')
    n7=request.POST.get('publisher')
    n8=request.POST.get('publish_time')
    if not n8:
        n8=datetime.datetime.now()
    n9=request.POST.get('page_number')
    n10=request.POST.get('words_number')
    n11=request.POST.get('add_time')
    if not n11:
        n11=datetime.datetime.now()
    n12=request.POST.get('editer_recommend')
    n13=request.POST.get('brief_introduction')
    n14=request.POST.get('author_introduction')
    n15=request.POST.get('catalogue')
    n16=request.POST.get('media_comments')
    n17=request.POST.get('tips_chapter')
    n18=request.POST.get('son')
    n19 = Category.objects.filter(title=n18)[0]
    n20=request.POST.get('edition')
    print(n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19)
    print(request.GET.get('flag'))
    #这里依然是get取值。
    if request.GET.get('flag'):

        try:
            with transaction.atomic():
                b=request.session.get('book')
                print(b)
                b.name=n1
                b.author=n2
                b.cover=n3
                b.market_price=n4
                b.dang_price=n5
                b.sales_amount=n6
                b.publisher=n7
                b.publish_time=n8
                b.page_number=n9
                b.words_number=n10
                b.editer_recomment=n12
                b.brief_introduction=n13
                b.author_introduction=n14
                b.catalogue=n15
                b.media_comments=n16
                b.tips_chapter=n17
                b.cate_id=n19
                b.add_time=n11
                b.edition=n20
                b1=Book.objects.filter(id=b.id)
                print(b,b1,b.name)
                b.save()
                #为什么修改了，数据库中没有改变
                n=Book.objects.filter(id=b.id)[0].name
                print(n)
                del request.session['book']
                return  redirect('user_admin:pro_list')
        except:
            return HttpResponse('wrong views85')
    try:
        with transaction.atomic():
            print('进入存储中，view50')
            b = Book.objects.create(name=n1, author=n2, cover=n3, market_price=n4, dang_price=n5,
                                    sales_amount=n6, publisher=n7, publish_time=n8, page_number=n9,
                                    words_number=n10, editer_recommend=n12, brief_introduction=n13,
                                    author_introduction=n14, catalogue=n15, media_comments=n16,
                                    tips_chapter=n17, cate_id=n19, add_time=n11, edition=n20)
            print('存储结束，view50', b.cover.url)
            return HttpResponse(b.cover.url)
    except:
        return HttpResponse('wrong view88')
def delete_book(request):

    num = request.GET.get('num')
    b=Book.objects.filter(id=num)
    print('进入删除',b)
    b.delete()
    print('删除了')
    return redirect('user_admin:pro_list')
def product_list(request):
    #设置页数，如果第一次没有取第一页，一页10行数据


    num = request.GET.get('num')
    print('i am here @120')
    if not num:
        num = 1
    b=Book.objects.all()
    amount=len(b)
    print(amount,'@view124')

    cate=Category.objects.all()
    page = Paginator(object_list=b, per_page=10).page(num)


    return render(request,'admin/list.html',{'book':b,'cate':cate,'page':page,'amount':amount})
def modify_product(request):
    #修改页面
    num=request.GET.get('num')
    cate=Category.objects.all()
    b=Book.objects.filter(id=num)
    b1=b[0]
    request.session['book']=b1
    c_book=Category.objects.filter(book__pk=num)[0]
    print(num,'81行',c_book,b1)
    return  render(request,'admin/modify.html',{'book':b,'cate':cate,'c':c_book,'b1':b1})
def cate_super(request):

    return  render(request,'admin/zjsp.html')
def super_logic(request):
    #增加父类逻辑判断
    cate=request.GET.get('cate')

    print(cate)
    try:
        with transaction.atomic():

            Category.objects.create(title=cate,parent_id=1)
            return redirect('/app_admin/category/list/?flag=1')
    except:
        return HttpResponse('error @ view150')
def cate_sub(request):
    #展示子类商品
    sup_cate = Category.objects.filter(parent_id=1)
    return  render(request,'admin/zjzlb.html',{'sup':sup_cate})
def sub_logic(request):
    #添加子商品逻辑
    cate=request.GET.get('cate')
    amount=request.GET.get('amount')
    cate_id=request.GET.get('cateid')
    cate_object=Category.objects.filter(title=cate_id)[0].id
    print(cate,cate_id)
    print(amount)
    print(cate_object)
    try:
        with transaction.atomic():
            print('存商品')
            Category.objects.create(title=cate,parent_id=cate_object,amount=amount)
            print('存商品成功')
            return redirect('/app_admin/category/list/?flag=1')

    except:
        return HttpResponse('error @ view165')
def delete_cate(request):
    #删除商品
    id = request.GET.get('id')
    num=request.GET.get('num')
    print(id,num)
    try:
        with transaction.atomic():
            Category.objects.filter(id=id).delete()
            print('删除成功 @view181')
            # 删除后将页面号码返回过去直接显示
            return redirect('/app_admin/category/list/?num='+num)
    except:
        return HttpResponse('error@view184')
def cate_list(request):
    #展示商品种类
    num=request.GET.get('num')
    print(num,'@204')
    if not num:
        num=1

    sup_cate=Category.objects.filter(parent_id=1)
    sub_cate=Category.objects.filter(parent_id__gt=1)
    n1=Paginator(object_list=sub_cate,per_page=5).num_pages
    #从添加种类过来的直接跳转到最后一页
    if request.GET.get('flag'):
        num=n1
    page = Paginator(object_list=sub_cate,per_page=5).page(num)

    print(sup_cate,sub_cate)
    return  render(request,'admin/splb.html',{'sup':sup_cate,'sub':sub_cate,'page':page})
def address_list(request):
    #展示用户与地址，由于外键需要展示两个
    ad=Address.objects.all()
    user=User.objects.all()
    order=Order.objects.all()
    amount=len(ad)
    num=request.GET.get('num')
    if not num:
        num=1
    page=Paginator(object_list=ad,per_page=5).page(num)
    return  render(request,'admin/dzlist.html',{'ad':ad,'user':user,'order':order,'page':page,'amount':amount})

def login_port(request):
    if request.GET.get('error'):
        error='请检查用户名与验证码是否正确'
        return render(request, 'admin/Signin.html', {'error': error})
    elif request.GET.get('flag'):
        #如果退出，删除session
        del request.session['admin']
    return render(request,'admin/Signin.html')

def login_logic(request):
    #设置登录逻辑
    u=request.POST.get('username')
    p=request.POST.get('password')
    re=request.POST.get('rem')
    captcha=request.POST.get('captcha')
    code = request.session.get('message_code')
    print(u,p,re,'admin-view@236',captcha,code)
    #这里就不判断收到验证码是否相同了，可以从上面打印可以看出，因为收费的。
    if User.objects.filter(username=u,password=p):
        response = redirect('user_admin:index')
        # 设置session保存
        request.session['admin'] = u
        if re:
            #设置cookie信息
            response.set_cookie(u,max_age=24*60*60)
        return response
    else:

        return redirect('/app_admin/page/login/?error=1')

def show(request):
    #进行测试手机验证码的页面
    return render(request,'admin/test1.html')

def phone(request):
    #登录手机验证码连接
    # 请求的路径
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    # 用户名是登录ihuyi.com账号名（例如：cf_demo123）
    account = "C03823094"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "385f386c45a350f05843faaf870e5a17"
    #设置手机验证码连接
    mobile=request.POST.get('mobile')
    code=random.sample(string.digits,4)
    code = ''.join(code)
    print('@250',mobile,code)
    # 拼接成发出的短信
    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = parse.urlencode(
        {'account': account, 'password':password, 'content': text, 'mobile': mobile, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    # 把验证码放进session中
    request.session['message_code'] = code
    print(eval(response_str.decode()))

    # 使用eval把字符串转为json数据返回
    return JsonResponse(eval(response_str.decode()))



