from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, List

from app.database import get_db
from app.models.user import User
from app.api.conversation import Conversation
from app.models.vocabulary import Vocabulary

router = APIRouter(prefix="/api/statistics", tags=["Statistics"])

@router.get("/overview")
async def get_study_overview(db: Session = Depends(get_db)):
    """전체 학습 통계 개요"""
    
    # 테스트용: 첫 번째 사용자
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 통계 계산
    total_conversations = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .count()
    
    total_words = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .count()
    
    mastered_words = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .filter(Vocabulary.is_mastered == True)\
        .count()
    
    return {
        "total_study_time": current_user.total_study_time,
        "total_conversations": total_conversations,
        "total_words": total_words,
        "mastered_words": mastered_words,
        "current_streak": current_user.current_streak,
        "target_language": current_user.target_language,
        "current_level": current_user.level
    }

@router.get("/today")
async def get_today_statistics(db: Session = Depends(get_db)):
    """오늘 학습 통계"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 오늘 날짜
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 오늘 대화 횟수
    today_conversations = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .filter(Conversation.timestamp >= today_start)\
        .count()
    
    # 오늘 추가한 단어
    today_words = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .filter(Vocabulary.created_at >= today_start)\
        .count()
    
    return {
        "date": today_start.strftime("%Y-%m-%d"),
        "conversations": today_conversations,
        "words_added": today_words,
        "study_time": 0,  # 추후 타이머 기능 추가 시
        "streak": current_user.current_streak
    }

@router.get("/weekly")
async def get_weekly_statistics(db: Session = Depends(get_db)):
    """주간 학습 통계 (지난 7일)"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 지난 7일 데이터
    week_data = []
    for i in range(6, -1, -1):
        date = datetime.utcnow() - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        # 해당 날짜의 대화 수
        conversations = db.query(Conversation)\
            .filter(Conversation.user_id == current_user.id)\
            .filter(and_(
                Conversation.timestamp >= date_start,
                Conversation.timestamp < date_end
            ))\
            .count()
        
        # 해당 날짜의 단어 수
        words = db.query(Vocabulary)\
            .filter(Vocabulary.user_id == current_user.id)\
            .filter(and_(
                Vocabulary.created_at >= date_start,
                Vocabulary.created_at < date_end
            ))\
            .count()
        
        week_data.append({
            "date": date_start.strftime("%Y-%m-%d"),
            "conversations": conversations,
            "words_added": words
        })
    
    return {
        "period": "last_7_days",
        "data": week_data
    }

@router.get("/progress")
async def get_learning_progress(db: Session = Depends(get_db)):
    """학습 진행도"""
    
    current_user = db.query(User).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    # 레벨별 목표
    level_goals = {
        "A1": {"conversations": 50, "words": 100},
        "A2": {"conversations": 100, "words": 200},
        "B1": {"conversations": 200, "words": 400},
        "B2": {"conversations": 400, "words": 800},
        "C1": {"conversations": 800, "words": 1500},
        "C2": {"conversations": 1500, "words": 3000}
    }
    
    current_level = current_user.level
    goal = level_goals.get(current_level, level_goals["A1"])
    
    total_conversations = db.query(Conversation)\
        .filter(Conversation.user_id == current_user.id)\
        .count()
    
    total_words = db.query(Vocabulary)\
        .filter(Vocabulary.user_id == current_user.id)\
        .count()
    
    conversation_progress = min(100, (total_conversations / goal["conversations"]) * 100)
    vocabulary_progress = min(100, (total_words / goal["words"]) * 100)
    
    return {
        "current_level": current_level,
        "conversations": {
            "current": total_conversations,
            "goal": goal["conversations"],
            "progress": round(conversation_progress, 1)
        },
        "vocabulary": {
            "current": total_words,
            "goal": goal["words"],
            "progress": round(vocabulary_progress, 1)
        },
        "overall_progress": round((conversation_progress + vocabulary_progress) / 2, 1)
    }