"""
Tests for Database Operations
"""
import pytest
from unittest.mock import Mock, MagicMock, patch


class TestDatabaseConnection:
    """Test database connection."""
    
    def test_init_db_creates_engine(self):
        """Test database initialization creates engine."""
        with patch('app.database.connection.create_engine') as mock_create:
            mock_create.return_value = MagicMock()
            
            from app.database.connection import init_db
            init_db()
            
            mock_create.assert_called()
    
    def test_get_db_session(self):
        """Test get_db session generation."""
        with patch('app.database.connection.SessionLocal') as mock_session:
            mock_session_instance = MagicMock()
            mock_session.return_value = mock_session_instance
            
            from app.database.connection import get_db
            gen = get_db()
            
            # Try to get first item
            try:
                next(gen)
            except StopIteration:
                pass


class TestCRUDOperations:
    """Test CRUD operations."""
    
    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return Mock()
    
    def test_create_analysis(self, mock_db):
        """Test creating analysis history."""
        from app.database.crud import create_analysis
        
        result = create_analysis(
            db=mock_db,
            code_hash="abc123",
            language="python",
            action="summarize",
            result="Test result"
        )
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_get_analysis_history(self, mock_db):
        """Test getting analysis history."""
        from app.database.crud import get_analysis_history
        
        mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = get_analysis_history(mock_db)
        
        assert isinstance(result, list)
    
    def test_get_analysis_by_hash(self, mock_db):
        """Test getting analysis by hash."""
        from app.database.crud import get_analysis_by_hash
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = get_analysis_by_hash(mock_db, "abc123", "summarize")
        
        assert result is None
    
    def test_create_snippet(self, mock_db):
        """Test creating code snippet."""
        from app.database.crud import create_snippet
        
        result = create_snippet(
            db=mock_db,
            name="test.py",
            code="print('hello')",
            language="python"
        )
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_get_snippets(self, mock_db):
        """Test getting code snippets."""
        from app.database.crud import get_snippets
        
        mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        result = get_snippets(mock_db)
        
        assert isinstance(result, list)
    
    def test_update_snippet(self, mock_db):
        """Test updating code snippet."""
        from app.database.crud import update_snippet, get_snippet_by_id
        
        mock_db.query.return_value.filter.return_value.first.return_value = Mock()
        
        result = update_snippet(mock_db, 1, name="updated.py")
        
        mock_db.commit.assert_called()
    
    def test_delete_snippet(self, mock_db):
        """Test deleting code snippet."""
        from app.database.crud import delete_snippet
        
        mock_db.query.return_value.filter.return_value.first.return_value = Mock()
        
        result = delete_snippet(mock_db, 1)
        
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called()


class TestModels:
    """Test database models."""
    
    def test_code_snippet_model(self):
        """Test CodeSnippet model creation."""
        from app.models.db_models import CodeSnippet
        
        # Basic attribute check
        assert hasattr(CodeSnippet, '__tablename__')
        assert CodeSnippet.__tablename__ == 'code_snippets'
    
    def test_analysis_history_model(self):
        """Test AnalysisHistory model creation."""
        from app.models.db_models import AnalysisHistory
        
        assert hasattr(AnalysisHistory, '__tablename__')
        assert AnalysisHistory.__tablename__ == 'analysis_history'
    
    def test_user_model(self):
        """Test User model creation."""
        from app.models.db_models import User
        
        assert hasattr(User, '__tablename__')
        assert User.__tablename__ == 'users'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
