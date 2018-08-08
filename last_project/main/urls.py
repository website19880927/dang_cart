from django.urls import path, include

from main import views

urlpatterns=[
    path('query/',include([
        path('all/',views.query_all,name='all'),
        path('one/',views.query_one,name='one'),
        path('list/',views.query_list,name='list'),

    ])),
    # path('ajax/',views.base,name='login_out')

]