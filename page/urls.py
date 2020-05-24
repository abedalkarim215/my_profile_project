from django.urls import path
from .views import *
urlpatterns = [
    path('profile/<str:username>',home,name='home'),
    path('ddd/',homePage,name='homePage'),



    path('add_service',add_service,name='add_service'),
    path('edit_service/<int:service_id>',edit_service,name='edit_service'),
    path('delete_service/<int:service_id>',delete_service,name='delete_service'),


    path('add_news/',add_news,name='add_news'),
    path('edit_news/<int:news_id>',edit_news,name='edit_news'),
    path('delete_news/<int:news_id>', delete_news, name='delete_news'),



    path('send_email/', send_email, name='send_email'),




    path('edit_informations',edit_informations,name='edit_informations'),
    path('news_details/<int:news_id>/',show_news_details,name='show_news_details'),
    # path('send',send_email,name='send_email'),
]
