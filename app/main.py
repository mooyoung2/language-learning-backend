from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import auth, conversation, vocabulary, statistics

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Language Learning AI API",
    description="AI 기반 언어 학습 앱 백엔드",
    version="1.0.0"
)

# CORS 설정 (Flutter 앱에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(conversation.router)
app.include_router(vocabulary.router)
app.include_router(statistics.router)

# 루트 엔드포인트
@app.get("/")
def root():
    return {
        "message": "Language Learning AI API",
        "version": "1.0.0",
        "status": "running"
    }

# 헬스체크
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
