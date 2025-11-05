from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 데이터베이스 URL
# SQLite (개발용 - 간단)
SQLALCHEMY_DATABASE_URL = "sqlite:///./language_learning.db"

# PostgreSQL (프로덕션용 - 나중에 사용)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/language_learning"

# SQLite 사용 시 connect_args 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()

# 데이터베이스 세션 의존성
def get_db():
    """
    데이터베이스 세션을 생성하고 요청 후 닫습니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 생성
def create_tables():
    """
    모든 테이블을 생성합니다.
    """
    Base.metadata.create_all(bind=engine)