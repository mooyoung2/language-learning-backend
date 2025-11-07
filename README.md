# Language Learning Backend API 🚀

AI 기반 언어 학습 애플리케이션 백엔드 API

## 📌 프로젝트 소개

FastAPI와 OpenAI GPT-3.5를 활용한 언어 학습 백엔드 시스템입니다.
사용자 관리, AI 대화, 단어장, 학습 통계 등의 기능을 RESTful API로 제공합니다.

## ✨ 주요 기능

### 1. 인증 (Authentication)
- 회원가입 / 로그인
- JWT 토큰 기반 인증
- 비밀번호 암호화 (bcrypt)

### 2. AI 대화 (Conversation)
- OpenAI GPT-3.5 연동
- 실시간 AI 튜터 대화
- 문법 교정 기능
- 대화 기록 저장

### 3. 단어장 (Vocabulary)
- 단어 CRUD (생성, 조회, 수정, 삭제)
- 난이도별 분류 (A1~C2)
- 마스터 단어 관리
- 단어장 통계

### 4. 학습 통계 (Statistics)
- 전체 학습 통계
- 일별/주간 통계
- 학습 진행도 추적
- 레벨별 목표 관리

## 🛠️ 기술 스택

- **Framework**: FastAPI 0.104.1
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT (python-jose)
- **Password**: bcrypt (passlib)
- **AI**: OpenAI GPT-3.5-turbo
- **Language**: Python 3.10+

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/language-learning-backend.git
cd language-learning-backend
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일 생성:
```env
DATABASE_URL=sqlite:///./language_learning.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. 서버 실행
```bash
python -m uvicorn app.main:app --reload
```

서버 실행 후: http://localhost:8000

## 📚 API 문서

서버 실행 후 자동 생성되는 Swagger UI에서 확인:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API 엔드포인트

### Authentication
```
POST   /api/auth/signup       # 회원가입
POST   /api/auth/login        # 로그인
GET    /api/auth/me           # 현재 사용자 조회
```

### Conversation
```
POST   /api/conversation/chat         # AI와 대화
GET    /api/conversation/history      # 대화 기록 조회
```

### Vocabulary
```
POST   /api/vocabulary                # 단어 추가
GET    /api/vocabulary                # 단어 목록 조회
GET    /api/vocabulary/review         # 복습 단어 조회
PUT    /api/vocabulary/{id}/master    # 마스터 처리
DELETE /api/vocabulary/{id}           # 단어 삭제
GET    /api/vocabulary/stats          # 단어장 통계
```

### Statistics
```
GET    /api/statistics/overview       # 전체 통계
GET    /api/statistics/today          # 오늘 통계
GET    /api/statistics/weekly         # 주간 통계
GET    /api/statistics/progress       # 학습 진행도
```

## 📂 프로젝트 구조
```
language_learning_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py             # DB 설정
│   ├── models/
│   │   ├── user.py             # 사용자 모델
│   │   └── vocabulary.py       # 단어 모델
│   ├── api/
│   │   ├── auth.py             # 인증 API
│   │   ├── conversation.py     # 대화 API
│   │   ├── vocabulary.py       # 단어장 API
│   │   └── statistics.py       # 통계 API
│   └── services/
│       └── openai_service.py   # OpenAI 서비스
├── .env                        # 환경 변수
├── .gitignore
├── requirements.txt            # 패키지 목록
└── README.md
```

## 🧪 테스트 계정
```
이메일: test@example.com
비밀번호: password123
```

## 🔐 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| DATABASE_URL | 데이터베이스 URL | sqlite:///./app.db |
| SECRET_KEY | JWT 비밀키 | your-secret-key |
| OPENAI_API_KEY | OpenAI API 키 | sk-... |

## 📊 데이터베이스 스키마

### Users
- id, name, email, password
- target_language, level
- total_conversations, total_words
- created_at, last_login

### Vocabularies
- id, user_id, word, meaning
- example, translation
- difficulty, is_mastered
- created_at, last_reviewed

### Conversations
- id, user_id
- user_message, ai_response
- grammar_correction
- timestamp

## 🚀 배포

### Heroku 배포 예시
```bash
heroku create your-app-name
git push heroku main
heroku config:set OPENAI_API_KEY=your-key
```

## 📝 라이선스

MIT License

## 👨‍💻 개발자

- **이름**: [당신 이름]
- **GitHub**: [당신 GitHub]
- **Email**: [당신 이메일]

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## 📮 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.
