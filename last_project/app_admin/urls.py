from django.urls import path, include

from app_admin import views

urlpatterns=[
    path('page/',include([
        path('login/',views.login_port,name='login'),
        path('logic/',views.login_logic,name='logic'),
        path('index/',views.index,name='index' ),
        path('add/',views.add,name='add'),
        path('list/',views.product_list,name='pro_list'),
        path('modify/',views.modify_product,name='modify'),
        path('delete/',views.delete_book,name='delete')

    ])),
    path('category/',include([
        path('super/',views.cate_super,name='super'),
        path('super_logic/',views.super_logic,name='super_logic'),
        path('sub/',views.cate_sub,name='sub'),
        path('sub_logic/',views.sub_logic,name='sub_logic'),
        path('delete/',views.delete_cate,name='delete_cate'),
        path('list/',views.cate_list,name='list')
    ])),
    path('ajax/',include([
        path('add_category/',views.ajax_add, name = 'ajax'),
        path('add_book/',views.add_logic,name='add_logic'),


    ])),

    path('addr/',views.address_list,name='address'),
    path('showphone/',views.show,name='show'),
    path('phone/',views.phone,name='phone'),

]