from django.db import models

# Create your models here.
from main.models import Book


class CartItem():
    def __init__(self,amount,book):
        self.amount=amount
        self.book=book
class Cart():
    def __init__(self):
        self.total_price=0
        self.save_money=0
        self.cartItem=[]
    def sums(self):
        self.total_price=0
        self.save_money=0
        for i in self.cartItem:
            self.total_price+=i.book[0].dang_price*i.amount
            self.save_money+=(i.book[0].market_price-i.book[0].dang_price)*i.amount
        print('我是书籍总价格models.22',self.total_price)
    def add(self,book_id):
        for i in self.cartItem:
            # print(type(book_id),type(i.book[0].id))
            #必须要转换 不然不一样，找不到错误 操蛋
            if i.book[0].id == book_id:
                print('购物车同样书籍，重复')
                i.amount+=1
                print(i.amount)
                self.sums()
                break
            # else:#如果购物车的id，没有，就添加这书
            #     book = Book.objects.filter(id=book_id)
            #     self.cartItem.append(CartItem(1, book))
            #     print('没有此书添加，id', book)
            #     self.sums()
        else:#如果购物车上面是空的 添加一本书
            book = Book.objects.filter(id=book_id)
            self.cartItem.append(CartItem(1, book))
            print('购物车没有，添加', book)
            self.sums()
            #     else:#如果购物车不是空的，同时id没有的话就添加
        #         book = Book.objects.filter(id=book_id)
        #         self.cartItem.append(CartItem(1, book))
        #         print('购物车有书，没有此书添加', book)
        #         self.sums()
        #     break
        # else:#如果购物车列表是空的，就直接添加一本
        #     print('购物车空的，添加一本书')
        #     book = Book.objects.filter(id=book_id)
        #     self.cartItem.append(CartItem(1,book))
        #     print(book)
        #     self.sums()
    def modify(self,bookid,amount):
        for i in self.cartItem:
            print('总数量',self.total_price,type(i.book[0].id),type(bookid))
            if i.book[0].id == bookid:
                i.amount=amount
                print('在修改中。。。')
                self.sums()
                print('修改后的数量',i.amount,self.total_price)
    def modify2(self,bookid,amount):
        for i in self.cartItem:
            print('总数量',self.total_price,type(i.book[0].id),type(bookid))
            if i.book[0].id == bookid:
                print(i.amount,'之前数量')
                #第一次创建书的时候数量加一，数量总是多一
                i.amount+=amount-1
                print('在修改中。。。')
                self.sums()
                print('修改后的数量',i.amount,self.total_price)
    def delete(self,bookid):
        for i in self.cartItem:
            if i.book[0].id==bookid:
                print('书籍存在，进入删除models.76',self.total_price)
                self.cartItem.remove(i)


        self.sums()
    # def sums(self):
    #     self.total_price=0
    #     self.save_money=0
    #     for i in self.cartItem:
#
# class Book_cart:
#     def __init__(self,book_id,book_name,book_price,nums,book_pic):
#         self.book_id=book_id
#         self.book_name=book_name
#         self.book_price=book_price
#         self.book_pic=book_pic
#
# class Cart:
#     def __init__(self):
#         self.cart={}
#         self.total_price=0
#         self.save_money=0
#         self.book_nums=0
#
#     def add(self,book):
#         if book.id not in self.cart:
#             self.cart[book.id]=book
#         else:
#             self.cart[book.id].nums=book.num





