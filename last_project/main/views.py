import hashlib

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from main.models import Category, Book

# def base(request):
#     if request.GET.get('key'):
#         del request.session['name']
#
#     return HttpResponse('退出登录')


def query_all(request):
    #获取登录后的session 传到页面，显示用户名
    name = request.session.get('name')
    b=Book.objects.all().order_by('publish_time')
    #显示没小页五本书b1,b2,b3
    b1=b[0:5]
    b2=b[6:11]
    b3=b[11:16]
    #cate1,cate2展示左边一级目录为1，由于是自连接，筛选所有的不是1的一级目录，
    #到页面中判断，如果二级目录的id与一级目录的id相同展示。
    cate1=Category.objects.filter(parent_id=1)
    cate2=Category.objects.filter(parent_id__gt=1)
    b=[b1,b2,b3]
    #选择十本销量高的显示页面
    amount=Book.objects.all().order_by('sales_amount')[0:10]
    # print(b,amount,name,cate1,cate2)

    #如果页面选择退出，则重新返回第一次没有name的页面，
    print(name,111)
    if request.GET.get('key'):
        if name:
            print(name, 333)
            del request.session['name']
            print(request.session.get('name'))
            re = {'cate1': cate1, 'cate2': cate2, 'book': b, 'amount': amount}
            return render(request, 'main/index.html', re)
        print(name,222)
    re={'cate1':cate1,'cate2':cate2,'book':b,'amount':amount,'name':name }
    return  render(request, 'main/index.html', re)


def query_one(request):
    name=request.session.get('name')
    if not name:
        name=''
    pk = request.GET.get('pk')
    if not pk:
        pk=1
    book=Book.objects.filter(pk=pk)
    cate=book[0].cate_id
    c_title=cate.title
    p_cate=Category.objects.filter(id=cate.parent_id)
    p_title=p_cate[0].title
    print(book[0],c_title,p_title,cate,name)
    re={'book':book[0],'c_title':c_title,'p_title':p_title,'cate':cate,'name':name}
    return render(request, 'main/Book details.html', re)


def query_list(request):
    name=request.session.get('name')
    num=request.GET.get('num')
    if not num:
        num = 1
    id = request.GET.get('id')
    sid = request.GET.get('sid')
    #注意这个sid 必须判断，不然一直空值出错，就与num一样，如果页码连接传过来一种有sid，一种没有sid ,没有sid就需要进行判断。
    if not sid:
        sid = 0
    # print(id,sid,num)
    cate = Category.objects.filter(parent_id=id)
    #获取一级分类 选择出来一个，直接cate1.title 展示 内容
    cate1 = Category.objects.filter(id=id)[0]
    flag = request.GET.get('flag')
    print(flag)
    # print(cate)
    # print(cate1)
    if sid:
        #如果二级分类存在，直接获取，同时书籍也直接可以获取，显示给用户
        cate2 = Category.objects.filter(id=sid)[0]
        print(cate2,'二级目录')

        if flag=='1':
            book=Book.objects.filter(cate_id=sid).order_by('-sales_amount')
            print(book)
            amount = len(book)
            page = Paginator(object_list=book, per_page=4).page(num)
            re = {'cate': cate, 'cate1': cate1, 'cate2': cate2, 'book': book, 'page': page, 'id': id, 'sid': sid,
                  'amount': amount,'name':name,'flag':flag}
            return render(request, 'main/booklist.html', re)
        elif flag=='2':
            book = Book.objects.filter(cate_id=sid).order_by('dang_price')
            amount = len(book)
            page = Paginator(object_list=book, per_page=4).page(num)
            re = {'cate': cate, 'cate1': cate1, 'cate2': cate2, 'book': book, 'page': page, 'id': id, 'sid': sid,
                  'amount': amount,'name':name,'flag':flag}
            return render(request, 'main/booklist.html', re)
        elif flag=='3':
            book = Book.objects.filter(cate_id=sid).order_by('publish_time')
            amount = len(book)
            page = Paginator(object_list=book, per_page=4).page(num)
            re = {'cate': cate, 'cate1': cate1, 'cate2': cate2, 'book': book, 'page': page, 'id': id, 'sid': sid,
                  'amount': amount,'name':name,'flag':flag}
            return render(request, 'main/booklist.html', re)

        book = Book.objects.filter(cate_id=sid)
        amount = len(book)
        page = Paginator(object_list=book, per_page=4).page(num)
        re = {'cate': cate, 'cate1': cate1, 'cate2': cate2, 'book': book, 'page': page, 'id': id, 'sid': sid,
              'amount': amount,'name':name,'flag':flag}
        return render(request, 'main/booklist.html', re)

    else:
        #如果只有一级类别，需要显示所有此类别下的图书，通过外键，取出，通过循环将每个类别中的元素
        #放入列表，传输过去，进行输出展示。
        l=[]
        for i in cate:
            all=i.book_set.all()
            for j in all:
                l.append(j)
        amount=len(l)
        page=Paginator(object_list=l,per_page=4).page(num)
        #利用sorted将其按照价格排序
        print('一级目录')
        if flag=='2':
            print('价格排序')
            p1 = sorted(l, key=lambda l: l.dang_price)
            page = Paginator(object_list=p1, per_page=4).page(num)
            re = {'name':name,'cate': cate, 'cate1': cate1, 'book': l, 'page': page, 'id': id, 'amount': amount,'flag':flag}
            return render(request, 'main/booklist.html', re)
        elif flag=='1':
            print('销量排序')
            a = sorted(l, key=lambda p: p.sales_amount,reverse=True)
            page = Paginator(object_list=a, per_page=4).page(num)
            print(page.object_list,111)
            re = {'name':name,'cate': cate, 'cate1': cate1, 'book': l, 'page': page, 'id': id, 'amount': amount,'flag':flag}
            return render(request, 'main/booklist.html', re)
        elif flag=='3':
            print('出版时间排序')
            pub = sorted(l, key=lambda p: p.publish_time)
            page = Paginator(object_list=pub, per_page=4).page(num)
            re = {'name':name,'cate': cate, 'cate1': cate1, 'book': l, 'page': page, 'id': id, 'amount': amount,'flag':flag}
            return render(request, 'main/booklist.html', re)
        print('默认排序')
        re = {'cate': cate, 'cate1': cate1,'book':l,'page':page,'id':id,'amount':amount,'name':name,'flag':flag}
        return  render_to_response('main/booklist.html',re)
#这里依然有问题，如果在大类中分类排序，第一页都没有问题，但是第二页第三页展示的时候就有问题了，由于这个时候不传递排列参数，因此就不
#不按照顺序排序了。

# def order(request):
#     n=request.GET.get('num')
#     s=request.GET.get('sale')
#     p=request.GET.get('price')
#     e=request.GET.get('publish')
#     sid=request.GET.get('sid')
#     id=request.GET.get('id')
#     page = Paginator(object_list=l, per_page=4).page(n)



# def hash_code(pwd,salt='password'):
#     h=hashlib.sha256()
#     pwd+=salt
#     h.update(pwd,encode())
#     return  h
