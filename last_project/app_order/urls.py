from django.urls import path, include

from app_order import views

urlpatterns=[
    path('cart/',include([
        path('page/', include([
            path('all/', views.cart, name='cart_page'),
            path('address/',views.address,name='address'),
            path('submit/',views.submit_ok,name='submit'),
        ])),
        path('ajax/',include([
            path('addlogic/',views.cart_logic,name='logic'),
            path('delete/',views.delete_cart,name='delete'),
            path('getall/',views.get_cart_sum,name='all'),
            path('delete_most/',views.delete_most,name='most'),
            path('show_add/',views.add_ajax,name='show_add'),
            path('change_select/',views.select_ajax,name='change_select'),
            path('back_cart/',views.back_cart,name='backcart'),
        ])),
        path('city/',views.city,name='city')
    ]))
]