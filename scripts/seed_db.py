"""
Database Seeding Script
Seed the database with initial data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import init_db, SessionLocal
from app.database.crud import create_snippet, create_analysis


def seed_sample_snippets():
    """Add sample code snippets to database."""
    snippets = [
        {
            "name": "Hello World Python",
            "code": "def hello():\n    print('Hello, World!')",
            "language": "python",
            "description": "Simple Hello World function"
        },
        {
            "name": "Hello World JavaScript",
            "code": "function hello() {\n    console.log('Hello, World!');\n}",
            "language": "javascript",
            "description": "Simple Hello World function"
        },
        {
            "name": "Factorial Function",
            "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
            "language": "python",
            "description": "Recursive factorial function"
        }
    ]
    
    db = SessionLocal()
    try:
        for snippet in snippets:
            create_snippet(
                db,
                name=snippet["name"],
                code=snippet["code"],
                language=snippet["language"],
                description=snippet["description"]
            )
        print(f"✓ Seeded {len(snippets)} sample snippets")
    except Exception as e:
        print(f"Error seeding snippets: {e}")
    finally:
        db.close()


def seed_sample_analyses():
    """Add sample analysis history."""
    analyses = [
        {
            "code_hash": "abc123",
            "language": "python",
            "action": "summarize",
            "result": "Test analysis result",
            "metadata": {"test": True}
        }
    ]
    
    db = SessionLocal()
    try:
        for analysis in analyses:
            create_analysis(
                db,
                code_hash=analysis["code_hash"],
                language=analysis["language"],
                action=analysis["action"],
                result=analysis["result"],
                metadata=analysis.get("metadata")
            )
        print(f"✓ Seeded {len(analyses)} sample analyses")
    except Exception as e:
        print(f"Error seeding analyses: {e}")
    finally:
        db.close()


def main():
    """Main seeding function."""
    print("Initializing database...")
    init_db()
    
    print("Seeding data...")
    seed_sample_snippets()
    seed_sample_analyses()
    
    print("✓ Database seeding complete!")


if __name__ == "__main__":
    main()
