from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db, Base

# Conversation 모델
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    grammar_correction = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="conversations")

from app.services.openai_service import OpenAIService
from app.models.user import User

router = APIRouter(prefix="/api/conversation", tags=["Conversation"])

# 요청 스키마
class ChatRequest(BaseModel):
    message: str

# 응답 스키마
class ChatResponse(BaseModel):
    ai_response: str
    grammar_correction: str | None = None
    tokens_used: int

# 사용자 인증 함수
async def get_current_user_from_header(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """헤더에서 사용자 인증"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다."
        )
    
    from jose import jwt, JWTError
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, "your-secret-key-change-this-in-production", algorithms=["HS256"])
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰")
            
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
            
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """AI와 대화하기 (테스트용)"""
    
    # 테스트용: 첫 번째 사용자 가져오기
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자가 없습니다")
    
    print(f"✅ 사용자: {current_user.name}, 언어: {current_user.target_language}")
    
    # OpenAI 서비스 호출
    openai_service = OpenAIService()
    result = await openai_service.chat_with_gpt(
        user_message=request.message,
        target_language=current_user.target_language,
        user_level=current_user.level
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    print(f"✅ GPT-3.5 응답: {result['ai_response'][:50]}...")
    
    # 대화 기록 저장
    conversation = Conversation(
        user_id=current_user.id,
        user_message=request.message,
        ai_response=result["ai_response"],
        grammar_correction=result.get("grammar_correction")
    )
    db.add(conversation)
    db.commit()
    
    return ChatResponse(
        ai_response=result["ai_response"],
        grammar_correction=result.get("grammar_correction"),
        tokens_used=result["tokens_used"]
    )

@router.get("/history")
async def get_conversation_history(
    db: Session = Depends(get_db),
    limit: int = 20
):
    """대화 기록 조회"""
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    conversations = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .order_by(Conversation.timestamp.desc())\
        .limit(limit)\
        .all()
    
    return {"conversations": conversations}