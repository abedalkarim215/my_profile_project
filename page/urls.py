from django.urls import path
from .views import *
urlpatterns = [


    path('profile/<str:username>',profile,name='profile'),
    path('',index,name='index'),





    path('add_service',add_service,name='add_service'),
    path('edit_service/<int:service_id>',edit_service,name='edit_service'),
    path('delete_service/<int:service_id>',delete_service,name='delete_service'),





    path('add_news/',add_news,name='add_news'),
    path('edit_news/<int:news_id>',edit_news,name='edit_news'),
    path('delete_news/<int:news_id>', delete_news, name='delete_news'),






    path('send_email/', send_email, name='send_email'),






    path('messages/', user_messages, name='user_messages'),
    path('message_details/<int:message_id>/', show_message, name='show_message'),
    path('delete_message/<int:message_id>', delete_message, name='delete_message'),
    path('delete_all_messages/', delete_all_messages, name='delete_all_messages'),




    path('replay/<int:receiver_id>/', user_replay, name='user_replay'),
    path('replay_message_details/<int:replay_message_id>/', show_replay_message, name='show_replay_message'),
    path('delete_replay/<int:replay_id>', delete_replay, name='delete_replay'),
    path('delete_all_replyes/', delete_all_replyes, name='delete_all_replyes'),
    path('reply_to_all/', reply_to_all, name='reply_to_all'),





    path('edit_informations/',edit_informations,name='edit_informations'),
    path('news_details/<int:news_id>/',show_news_details,name='show_news_details'),



]
