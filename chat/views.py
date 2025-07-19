import requests
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.utils import timezone
from .serializers import ChatSerializer, DiscordMessageSerializer, ReceivedMessageSerializer
from .models import DiscordMessage, ReceivedMessage
from drf_yasg.utils import swagger_auto_schema

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1395994907176603738/vjPEwDIakkDtrFK4W_MFdaTgT5FwqNw35pi-YEOra6TZ8x5LvkbuPW-0WXOjpKd49hrp'

@swagger_auto_schema(method='post', request_body=ChatSerializer)
@api_view(['POST'])
@csrf_exempt
def chat_api(request):
    serializer = ChatSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        
        # DB에 메시지 저장
        discord_message = DiscordMessage.objects.create(
            content=message,
            is_sent=False
        )
        
        # Discord로 메시지 전송
        payload = {'content': message}
        try:
            r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
            if r.status_code == 204:
                # 성공 시 상태 업데이트
                discord_message.is_sent = True
                discord_message.save()
                return Response({
                    'detail': 'Message sent successfully',
                    'message_id': discord_message.id
                }, status=status.HTTP_200_OK)
            else:
                # 실패 시 에러 메시지 저장
                discord_message.error_message = f"Discord API returned status {r.status_code}"
                discord_message.save()
                return Response({
                    'detail': 'Failed to send message to Discord',
                    'error': f"Status code: {r.status_code}"
                }, status=status.HTTP_502_BAD_GATEWAY)
        except requests.exceptions.RequestException as e:
            # 네트워크 에러 시 에러 메시지 저장
            discord_message.error_message = str(e)
            discord_message.save()
            return Response({
                'detail': 'Network error occurred',
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: DiscordMessageSerializer(many=True)})
@api_view(['GET'])
@csrf_exempt
def message_list(request):
    """메시지 목록을 조회합니다."""
    messages = DiscordMessage.objects.all()[:50]  # 최근 50개만 조회
    serializer = DiscordMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["POST"])
def discord_webhook_receiver(request):
    """Discord webhook을 받아서 메시지를 저장합니다."""
    try:
        data = json.loads(request.body)
        
        # Discord webhook 데이터 파싱
        if 'type' in data and data['type'] == 1:  # PING
            return Response({'type': 1}, status=status.HTTP_200_OK)
        
        if 'type' in data and data['type'] == 0:  # MESSAGE
            message_data = data.get('d', {})
            
            # 봇 메시지도 받기 (필터링 제거)
            # if message_data.get('author', {}).get('bot', False):
            #     return Response({'status': 'bot message ignored'}, status=status.HTTP_200_OK)
            
            # 메시지 저장
            received_message = ReceivedMessage.objects.create(
                username=message_data.get('author', {}).get('username', 'Unknown'),
                content=message_data.get('content', ''),
                channel_id=message_data.get('channel_id', ''),
                message_id=message_data.get('id', '')
            )
            
            return Response({
                'status': 'message saved',
                'message_id': received_message.id
            }, status=status.HTTP_200_OK)
        
        return Response({'status': 'unknown message type'}, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='get', responses={200: ReceivedMessageSerializer(many=True)})
@api_view(['GET'])
@csrf_exempt
def received_message_list(request):
    """받은 메시지 목록을 조회합니다."""
    messages = ReceivedMessage.objects.all()[:10]  # 최근 50개만 조회
    serializer = ReceivedMessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def received_messages_page(request):
    """받은 메시지 목록을 HTML 페이지로 보여줍니다."""
    messages = ReceivedMessage.objects.all()[:10]
    return render(request, 'chat/received_messages.html', {
        'messages': messages,
        'message_count': messages.count()
    })

def sent_messages_page(request):
    """보낸 메시지 목록을 HTML 페이지로 보여줍니다."""
    messages = DiscordMessage.objects.all()[:10]
    return render(request, 'chat/sent_messages.html', {
        'messages': messages,
        'message_count': messages.count()
    })

@api_view(['POST'])
@csrf_exempt
def create_test_message(request):
    """테스트용 받은 메시지를 생성합니다."""
    try:
        test_message = ReceivedMessage.objects.create(
            username="테스트 사용자",
            content="이것은 테스트 메시지입니다! " + timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            channel_id="123456789",
            message_id="test_" + str(int(timezone.now().timestamp()))
        )
        return Response({
            'detail': 'Test message created successfully',
            'message_id': test_message.id
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
