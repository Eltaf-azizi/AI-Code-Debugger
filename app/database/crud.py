"""
CRUD Operations
Database create, read, update, delete operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON


class AnalysisHistory(Base):
    """Analysis history model."""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    code_hash = Column(String(64), index=True)
    language = Column(String(50))
    action = Column(String(50))
    result = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class CodeSnippet(Base):
    """Code snippet storage."""
    __tablename__ = "code_snippets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    code = Column(Text)
    language = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============== Analysis History CRUD ==============

def create_analysis(
    db: Session,
    code_hash: str,
    language: str,
    action: str,
    result: str,
    metadata: Optional[dict] = None
) -> AnalysisHistory:
    """Create analysis history entry."""
    analysis = AnalysisHistory(
        code_hash=code_hash,
        language=language,
        action=action,
        result=result,
        metadata=metadata
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_analysis_history(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[AnalysisHistory]:
    """Get analysis history."""
    return db.query(AnalysisHistory)\
        .order_by(AnalysisHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_analysis_by_hash(
    db: Session,
    code_hash: str,
    action: str
) -> Optional[AnalysisHistory]:
    """Get analysis by code hash and action."""
    return db.query(AnalysisHistory)\
        .filter(
            AnalysisHistory.code_hash == code_hash,
            AnalysisHistory.action == action
        )\
        .first()


# ============== Code Snippet CRUD ==============

def create_snippet(
    db: Session,
    name: str,
    code: str,
    language: str,
    description: Optional[str] = None
) -> CodeSnippet:
    """Create code snippet."""
    snippet = CodeSnippet(
        name=name,
        code=code,
        language=language,
        description=description
    )
    db.add(snippet)
    db.commit()
    db.refresh(snippet)
    return snippet


def get_snippets(
    db: Session,
    language: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[CodeSnippet]:
    """Get code snippets."""
    query = db.query(CodeSnippet)
    
    if language:
        query = query.filter(CodeSnippet.language == language)
    
    return query\
        .order_by(CodeSnippet.updated_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_snippet_by_id(db: Session, snippet_id: int) -> Optional[CodeSnippet]:
    """Get snippet by ID."""
    return db.query(CodeSnippet).filter(CodeSnippet.id == snippet_id).first()


def update_snippet(
    db: Session,
    snippet_id: int,
    name: Optional[str] = None,
    code: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[CodeSnippet]:
    """Update code snippet."""
    snippet = get_snippet_by_id(db, snippet_id)
    
    if snippet:
        if name is not None:
            snippet.name = name
        if code is not None:
            snippet.code = code
        if description is not None:
            snippet.description = description
        
        db.commit()
        db.refresh(snippet)
    
    return snippet


def delete_snippet(db: Session, snippet_id: int) -> bool:
    """Delete code snippet."""
    snippet = get_snippet_by_id(db, snippet_id)
    
    if snippet:
        db.delete(snippet)
        db.commit()
        return True
    
    return False
