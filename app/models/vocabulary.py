from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.database import get_db, Base

# Vocabulary 모델
class Vocabulary(Base):
    __tablename__ = "vocabularies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word = Column(String, nullable=False, index=True)
    meaning = Column(String, nullable=False)
    example = Column(String)
    translation = Column(String)
    language = Column(String, default="영어")
    difficulty = Column(String, default="A1")
    is_mastered = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    
    # 관계 추가!
    user = relationship("User", back_populates="vocabularies")

from app.models.user import User

router = APIRouter(prefix="/api/vocabulary", tags=["Vocabulary"])

# 요청 스키마
class VocabularyCreate(BaseModel):
    word: str
    meaning: str
    example: Optional[str] = None
    translation: Optional[str] = None
    difficulty: Optional[str] = "A1"

class VocabularyUpdate(BaseModel):
    is_mastered: bool

# 응답 스키마
class VocabularyResponse(BaseModel):
    id: int
    word: str
    meaning: str
    example: Optional[str]
    translation: Optional[str]
    language: str
    difficulty: str
    is_mastered: bool
    review_count: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=VocabularyResponse)
async def add_vocabulary(
    vocab: VocabularyCreate,
    db: Session = Depends(get_db)
):
    """단어 추가"""
    
    # 테스트용: 첫 번째 사용자
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 단어 생성
    new_vocab = Vocabulary(
        user_id=current_user.id,
        word=vocab.word,
        meaning=vocab.meaning,
        example=vocab.example,
        translation=vocab.translation,
        language=current_user.target_language,
        difficulty=vocab.difficulty
    )
    
    db.add(new_vocab)
    db.commit()
    db.refresh(new_vocab)
    
    print(f"✅ 단어 추가: {new_vocab.word}")
    
    return new_vocab

@router.get("/", response_model=List[VocabularyResponse])
async def get_vocabularies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    mastered: Optional[bool] = None
):
    """단어 목록 조회"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    query = db.query(Vocabulary).filter(Vocabulary.user_id == current_user.id)
    
    if mastered is not None:
        query = query.filter(Vocabulary.is_mastered == mastered)
    
    vocabularies = query.order_by(Vocabulary.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return vocabularies

@router.get("/review", response_model=List[VocabularyResponse])
async def get_review_vocabularies(
    db: Session = Depends(get_db),
    limit: int = 20
):
    """복습 필요한 단어 조회"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    vocabularies = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .filter(Vocabulary.is_mastered == False)\
        .order_by(Vocabulary.review_count.asc())\
        .limit(limit)\
        .all()
    
    return vocabularies

@router.put("/{vocab_id}/master", response_model=VocabularyResponse)
async def mark_as_mastered(
    vocab_id: int,
    update: VocabularyUpdate,
    db: Session = Depends(get_db)
):
    """단어 마스터 처리"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    vocab = db.query(Vocabulary)\
        .filter(Vocabulary.id == vocab_id)\
        .filter(Vocabulary.user_id == current_user.id)\
        .first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="단어를 찾을 수 없습니다")
    
    vocab.is_mastered = update.is_mastered
    vocab.review_count += 1
    vocab.last_reviewed = datetime.utcnow()
    
    db.commit()
    db.refresh(vocab)
    
    print(f"✅ 단어 마스터 처리: {vocab.word} - {update.is_mastered}")
    
    return vocab

@router.delete("/{vocab_id}")
async def delete_vocabulary(
    vocab_id: int,
    db: Session = Depends(get_db)
):
    """단어 삭제"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    vocab = db.query(Vocabulary)\
        .filter(Vocabulary.id == vocab_id)\
        .filter(Vocabulary.user_id == current_user.id)\
        .first()
    
    if not vocab:
        raise HTTPException(status_code=404, detail="단어를 찾을 수 없습니다")
    
    word = vocab.word
    db.delete(vocab)
    db.commit()
    
    print(f"✅ 단어 삭제: {word}")
    
    return {"message": f"'{word}' 단어가 삭제되었습니다"}

@router.get("/stats")
async def get_vocabulary_stats(db: Session = Depends(get_db)):
    """단어장 통계"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    total = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .count()
    
    mastered = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .filter(Vocabulary.is_mastered == True)\
        .count()
    
    learning = total - mastered
    
    return {
        "total_words": total,
        "mastered_words": mastered,
        "learning_words": learning,
        "mastery_rate": round((mastered / total * 100) if total > 0 else 0, 1)
    }