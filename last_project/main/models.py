# from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class User(models.Model):
    # user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    class Meta:
        db_table='t_user'

class  MyString:

    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ascii_letters = ascii_lowercase + ascii_uppercase
    digits = '0123456789'
    hexdigits = digits + 'abcdef' + 'ABCDEF'
    octdigits = '01234567'
    punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    han='你是王八蛋'


class Order(models.Model):
    user_id = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True)
    sum_money = models.FloatField()
    recipient = models.CharField(max_length=20)
    site = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)

    class Meta:
        db_table = 't_order'

class Category(models.Model):
    title=models.CharField(max_length=20)
    parent_id=models.FloatField(null=True)
    amount=models.BigIntegerField(null=True)
    class Meta:
        db_table='t_category'


class Book(models.Model):
    name=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    cover = models.ImageField(upload_to='book_cover', null=True)
    market_price=models.FloatField()
    dang_price=models.FloatField()
    sales_amount=models.BigIntegerField()
    publisher=models.CharField(max_length=20)
    publish_time=models.DateField()
    page_number=models.IntegerField()
    edition=models.IntegerField()
    words_number=models.BigIntegerField()
    add_time=models.DateTimeField(auto_now_add=True)
    editer_recommend=models.TextField()
    brief_introduction=models.TextField()
    author_introduction = models.TextField()
    catalogue = models.TextField()
    media_comments=models.TextField()
    tips_chapter=models.TextField()
    cate_id=models.ForeignKey(to='Category',on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table='t_book'

class OrderItem(models.Model):
    order_id = models.ForeignKey(to='Order', on_delete=models.SET_NULL, null=True)
    book_id = models.ForeignKey(to='Book', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    subtotal = models.FloatField()

    class Meta:
        db_table = 't_orderitem'


class Address(models.Model):
    recipient = models.CharField(max_length=20)
    site = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20)
    user_id = models.ForeignKey(to='User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 't_address'

