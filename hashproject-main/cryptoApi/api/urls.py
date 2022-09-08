from django.urls import path

from . import views

urlpatterns = [
    path('list', views.view_list, name='list'),
    path('detail/<id>', views.view_detail, name='detail'),
    path('hashList', views.view_algo_list_scrapping, name='hashList'),
    path('coinList/<id>', views.view_coin_list, name='hashList'),
    path('algoList', views.view_algo_list, name='hashList'),
    path('coinDetail/<type>/<id>', views.view_coin_detail, name='hashList'),
    path('coinListCelery', views.view_coin_list_celery, name='hashList'),
]


