# Discord Webhook API

Discord webhook을 통해 메시지를 전송하고 받는 Django REST API 프로젝트입니다.

## 기능

- Discord webhook을 통한 메시지 전송
- Discord webhook을 통한 메시지 수신 및 저장
- 메시지 히스토리 저장 및 조회 (보낸 메시지, 받은 메시지)
- Swagger UI를 통한 API 문서화
- 메시지 전송 상태 추적

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 서버 실행
```bash
python manage.py runserver
```

## API 엔드포인트

### 메시지 전송
- **URL**: `POST /api/v1/chat/`
- **Content-Type**: `application/json`
- **Body**:
```json
{
    "message": "전송할 메시지"
}
```

### 보낸 메시지 목록 조회
- **URL**: `GET /api/v1/messages/`
- **Response**: 최근 50개 보낸 메시지 목록

### 받은 메시지 목록 조회
- **URL**: `GET /api/v1/received-messages/`
- **Response**: 최근 50개 받은 메시지 목록

### Discord Webhook 수신
- **URL**: `POST /api/v1/webhook/`
- **Content-Type**: `application/json`
- Discord에서 메시지가 올 때마다 자동으로 호출되어 DB에 저장

## API 문서

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## 데이터베이스 설정

### SQLite (기본)
현재 SQLite를 사용하도록 설정되어 있습니다.

### MySQL 사용 시
1. `requirements.txt`에서 `mysqlclient` 주석 해제
2. `settings.py`에서 MySQL 설정 주석 해제
3. MySQL 서버 설정 및 데이터베이스 생성

## 모델 구조

### DiscordMessage (보낸 메시지)
- `content`: 메시지 내용 (최대 2000자)
- `created_at`: 생성 시간
- `is_sent`: 전송 성공 여부
- `error_message`: 에러 메시지 (실패 시)

### ReceivedMessage (받은 메시지)
- `username`: 메시지 작성자 이름
- `content`: 메시지 내용 (최대 2000자)
- `received_at`: 수신 시간
- `channel_id`: Discord 채널 ID
- `message_id`: Discord 메시지 ID

## 관리자 페이지

- **URL**: `http://localhost:8000/admin/`
- 보낸 메시지와 받은 메시지 히스토리 확인 및 관리 가능

## Discord Webhook 설정

### 메시지 전송용 Webhook
- `chat/views.py`의 `DISCORD_WEBHOOK_URL` 설정

### 메시지 수신용 Webhook
1. Discord 서버에서 봇 생성
2. 봇에 메시지 읽기 권한 부여
3. Webhook URL을 `http://your-domain.com/api/v1/webhook/`로 설정

## 환경 설정

- `DEBUG`: 개발 모드 (True)
- `ALLOWED_HOSTS`: 모든 호스트 허용 (`['*']`)
- Discord Webhook URL은 `chat/views.py`에서 설정

## 전체 기능 요약

### 1. 메시지 전송 기능
- Discord로 메시지 전송
- 전송 상태 추적 및 에러 처리
- DB에 전송 기록 저장

### 2. 메시지 수신 기능
- Discord webhook을 통한 메시지 수신
- 사용자 이름, 내용, 시간 자동 저장
- 봇 메시지 자동 필터링

### 3. 메시지 관리 기능
- 보낸 메시지/받은 메시지 분리 저장
- 최근 50개 메시지 조회
- 관리자 페이지에서 전체 히스토리 확인

### 4. API 문서화
- Swagger UI로 실시간 API 테스트
- ReDoc으로 API 문서 확인
