from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Для Docker
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/warehouse"

# Для локального запуска без Docker
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/warehouse"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
