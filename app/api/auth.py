from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Pydantic 모델 (요청/응답 스키마)
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    target_language: str = "영어"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    target_language: str
    level: str
    total_study_time: int
    total_conversations: int
    total_words_learned: int
    current_streak: int

    class Config:
        from_attributes = True


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    회원가입
    """
    # 이메일 중복 확인
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(user_data.password)
    
    # 새 사용자 생성
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        target_language=user_data.target_language
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.name,
            "target_language": new_user.target_language,
            "level": new_user.level
        }
    }


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    로그인
    """
    # 사용자 찾기
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    # 비밀번호 확인
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "target_language": user.target_language,
            "level": user.level,
            "total_study_time": user.total_study_time,
            "total_conversations": user.total_conversations,
            "total_words_learned": user.total_words_learned,
            "current_streak": user.current_streak
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    """
    현재 로그인한 사용자 정보 가져오기
    """
    from app.utils.auth import decode_access_token
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    return user