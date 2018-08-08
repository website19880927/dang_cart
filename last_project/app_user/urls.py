from django.urls import path, include

from app_user import views

urlpatterns=[
    path('login/',include([
        path('port/',views.login_page,name='login'),
        path('logic/',views.login_logic,name='logic'),
    ])),
    path('ajax/',include([
        path('name/',views.ajax,name='ajax')
    ])),
    path('regist/',include([
        path('port/',views.regist,name='regist'),
        path('logic/',views.regist_logic,name='regist_logic')
    ])),
    path('captcha/',include([
        path('image/',views.capta,name='captcha')
    ]))

]