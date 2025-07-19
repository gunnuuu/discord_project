from django.urls import path
from .views import chat_api, message_list, discord_webhook_receiver, received_message_list, received_messages_page, sent_messages_page, create_test_message

urlpatterns = [
    path('chat/', chat_api, name='chat_api'),  # /api/v1/chat/ 로 접근 가능
    path('messages/', message_list, name='message_list'),  # /api/v1/messages/ 로 접근 가능
    path('webhook/', discord_webhook_receiver, name='discord_webhook_receiver'),  # /api/v1/webhook/ 로 접근 가능
    path('received-messages/', received_message_list, name='received_message_list'),  # /api/v1/received-messages/ 로 접근 가능
    path('create-test-message/', create_test_message, name='create_test_message'),  # 테스트 메시지 생성
    
    # HTML 페이지
    path('received-messages-page/', received_messages_page, name='received_messages_page'),  # 받은 메시지 HTML 페이지
    path('sent-messages-page/', sent_messages_page, name='sent_messages_page'),  # 보낸 메시지 HTML 페이지
]
