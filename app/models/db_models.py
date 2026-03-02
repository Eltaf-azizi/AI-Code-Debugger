"""
Database Models
SQLAlchemy models for database tables
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.connection import Base


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    snippets = relationship("CodeSnippet", back_populates="owner")
    analyses = relationship("AnalysisHistory", back_populates="user")


class CodeSnippet(Base):
    """Code snippet storage model."""
    __tablename__ = "code_snippets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="snippets")
    tags = relationship("SnippetTag", back_populates="snippet")


class AnalysisHistory(Base):
    """Analysis history model."""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    code_hash = Column(String(64), index=True)
    language = Column(String(50))
    action = Column(String(50), index=True)  # summarize, debug, explain, etc.
    result = Column(Text)
    metadata = Column(JSON)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="analyses")


class Tag(Base):
    """Tag model for categorizing snippets."""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(7))  # Hex color code
    
    # Relationships
    snippets = relationship("SnippetTag", back_populates="tag")


class SnippetTag(Base):
    """Many-to-many relationship between snippets and tags."""
    __tablename__ = "snippet_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    snippet_id = Column(Integer, ForeignKey("code_snippets.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    
    # Relationships
    snippet = relationship("CodeSnippet", back_populates="tags")
    tag = relationship("Tag", back_populates="snippets")


class Project(Base):
    """Project model for grouping related code files."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(50))
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    files = relationship("ProjectFile", back_populates="project")


class ProjectFile(Base):
    """Individual file within a project."""
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    language = Column(String(50))
    content = Column(Text)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="files")


class ApiKey(Base):
    """API key model for programmatic access."""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
