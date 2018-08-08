import json

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from app_order.models import Cart, CartItem
from app_user.models import Cities, Province, Areas

from main.models import Book, Address, User, Order, OrderItem


def cart(request):

    cart=request.session.get('cart')
    name=request.session.get('name')
    print(cart,cart.total_price)
    if not cart:
        return redirect('main:all')
    else:

        # print(cart, type(cart))

        total = cart.total_price
        save = cart.save_money
        items = cart.cartItem
        print(total,save,items,cart)

        amount2=len(cart.cartItem)
        re={'amount1':amount2,'total':total,'save':save,'cart':cart,'item':items,'name':name}
#之前寫錯了，将重复的书籍都加入到购物车中了，
        return render(request,'order/car.html',re)

def delete_most(request):
    cart = request.session.get('cart')
    pk = request.GET.get('pk')
    pk=pk.split(',')
    #注意传过来的是 字符串，这里继续分割，注意分割的时候需要接收，
    print('most view:34' ,pk,type(pk))
    for i in pk:
        pk=int(i)
        print(pk)
        print(' view:37删除前的购物车价格总',cart.total_price)
        cart.delete(pk)
        # print('删除后的购物车价格总 view:39', cart.total_price)
        request.session['cart'] = cart
    total = cart.total_price
    print('view.42删除后价格', total)
    save = cart.save_money
    re = {'total1': total, 'save1': save}
    return JsonResponse(re)
def delete_cart(request):

    cart=request.session.get('cart')
    pk=int(request.GET.get('pk'))


    print('view.34我是删除前的价格',cart.total_price,pk)
    cart.delete(pk)
    request.session['cart']=cart
    #只要发生修改就需要修改session
    total = cart.total_price
    print('view.37删除后价格',total)
    save = cart.save_money
    re = {'total1': total, 'save1': save}
    return JsonResponse(re)
def get_cart_sum(request):
    #必须将类型转换一下 ，这里又搞错了
    book_id=int(request.GET.get('pk'))
    per_amount=int(request.GET.get('amount'))
    print(book_id,per_amount)
    cart=request.session.get('cart')
    cart.modify(book_id,per_amount)
    total = cart.total_price
    save = cart.save_money
    print(total,save)
    re={'total1':total,'save1':save}
    return JsonResponse(re)

def cart_logic(request):
    book_id=int(request.GET.get('pk'))
    #下面的改了好几次又不记得了，由于从booklist传过来的是一本，设置amount为1
    # am0=request.GET.get('amount')
    # if not am0:
    #     am0=1
    # am=int(am0)
    am = int(request.GET.get('amount'))
    cart=request.session.get('cart')
    print(book_id,cart,am)
    #有两种跳转方式，一种是booklist到来，没有amount，只要一本的数量，因此需要将这个置一，
    #第二种跳转是从单本书页面跳转过来，有两数据，数id与数的数量，有数量就执行下面的。
#如果第一次购物车是空的 ，直接创造对象购物车，添加书籍
    if not cart:
        cart=Cart()
        cart.add(book_id)
        request.session['cart'] = cart
        print(cart)#如果传多本书，第一次传没有购物车，需要创建购物车，同时修改数量
        if am >= 2:
            print('第一次没有购物车，创建购物车，数量多本',am)
            cart.modify2(book_id, am)

            request.session['cart'] = cart

    #将购物车里面的内容存入session，主要是amount与book对象
        request.session['cart']=cart
#第二次往后购物车都存在，就直接在购物车中添加就可以
    else:
        cart.add(book_id)
        request.session['cart'] = cart
        if am >= 2:
            print('存在购物车',cart.total_price)
            cart.modify2(book_id, am)
            # cart.add(book_id)

            request.session['cart'] = cart

    return HttpResponse('ok')

def back_cart(request):
    cart = request.session.get('cart')
    pk = int(request.GET.get('pk'))
    print('view.124我是删除前的价格', cart.total_price, pk)
    cart.delete(pk)
    request.session['cart'] = cart
    # 只要发生修改就需要修改session
    total = cart.total_price
    print('view.37删除后价格', total)
    save = cart.save_money
    #同时需要将选择的物品存放到新的购物车上面放入session存储。
    cart2=Cart()
    cart2.add(pk)
    request.session['cart2']=cart2
    re = {'total1': total, 'save1': save}
    return JsonResponse(re)

def address(request):
    #判读是否登录，如果没有登录标志登录在跳转回去登录后再到这个界面
    name=request.session.get('name')
    if not name:
        #如果提交后发现没有登录的用户名session，则跳转到登录界面，同时将标志位flag带过去
        #说明是从提交地址界面过来的
        print('没有登录回去登录')
        return redirect('/user/login/port/?flag=5')
    print('登录过了')
    #这里需要传一个旧地址参数
    #先将user_id查出来
    # print(user_id)见下面的add_ajax
    #利用name查询这个用户的地址信息，这里只是返回给用户一个筛选框，如果对方点击后，需要单击返回json,ajax再次建立view
    add=Address.objects.filter(user_id__username=name)
    cart=request.session.get('cart')
    total=cart.total_price
    items=cart.cartItem
    # 这里需要将产生的订单保存到数据库中
    try:
        with transaction.atomic():
            for i in items:
                #这里也需要注意 添加id是外键书的对象。
                id=i.book[0]
                amount=i.amount
                price=i.book[0].dang_price
                per_price=int(amount)*int(price)
                print(id,amount,price,per_price)
                #添加订单，由于这个时候地址订单没有产生，所以暂时不添加order_id,在结算结束地址产生后，再关联吧。
                OrderItem.objects.create(book_id=id,quantity=amount,unit_price=price,subtotal=per_price)
            re = {'cart': cart, 'total': total, 'add': add, 'name': name}
            return render(request, 'order/address.html', re)

    except:
        return  HttpResponse('添加订单错误，重新添加')
    #

def add_ajax(request):
    ad=request.GET.get('show_add')
    add = Address.objects.filter(site=ad).values()
    all_add=list(add)
    #这里注意返回中文，需要使用json.dumps 设置编码
    json_str=json.dumps(all_add,ensure_ascii=False)
    return HttpResponse(json_str)
    # return  JsonResponse(all_add,safe=False,ensure_ascii=False)
def select_ajax(request):
    n1=request.GET.get('change')

    if request.GET.get('flag'):

        p_ob = Cities.objects.filter(city=n1)[0].cityid
        print(p_ob)
        city = list(Areas.objects.filter(cityid=p_ob).values())
        print(city)
    else:
        p_ob = Province.objects.filter(province=n1)[0].provinceid
        print(p_ob)
        city = list(Cities.objects.filter(provinceid=p_ob).values())
        print(city)
    json_str=json.dumps(city,ensure_ascii=False)
    return  HttpResponse(json_str)
    # return JsonResponse(city ,safe=False)



def submit_ok(request):
    #这里判读
    cart=request.session.get('cart')
    total_price=cart.total_price
    amount=len(cart.cartItem)
    name = request.session.get('name')
    r=request.GET.get('receiver')
    d=request.GET.get('detail')
    po=request.GET.get('po')
    ph=request.GET.get('ph')
    #注意这里的外键必须是一个对象 如果添加必须添加这个用户对象
    u_id=User.objects.filter(username=name)[0]
    print(r,d,po,ph,u_id)
    try:
        with transaction.atomic():
            #添加地址表
            Address.objects.create(recipient=r,site=d,zip_code=po,telephone=ph,user_id=u_id)
            #添加订单表
            o=Order.objects.create(user_id=u_id,sum_money=total_price,recipient=r,site=d,zip_code=po,telephone=ph)
            #修改订单项目表中对应的订单地址id的关联，将对象进行保存。
            print('地址订单，保存中。')
            oi = OrderItem.objects.all()
            for i in oi:
                print(i)
                i.order_id = o
                i.save()
            #这里提交结束订单后将购物车删除。
            del request.session['cart']
            #删除后，如果上一步有用户后悔不想买了，将订单中的东西又放回购物车中，这时候需要再次将购物车
            #重新赋值存入session，以便再次打开购物车中依然有东西。
            if request.session.get('cart2'):
                request.session['cart']=request.session.get('cart2')
            return render(request, 'order/indent ok.html',{'total':total_price,'name': name, 'id': u_id.pk, 'amount': amount, 'to_name': r})


    except:
        # return redirect('order:address')
        return  HttpResponse('地址错误，重新添加')

def city(request):
    all=Cities.objects.all()
    print(all)
    return render(request,'order/add1.html')
