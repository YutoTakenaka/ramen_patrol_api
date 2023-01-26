from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dbの格納先
SQLALCHEMY_DATABASE_URL = 'sqlite:///./ramen_patrol_api.db'

# crud操作の基盤となる部分
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False}
)

# sessionのいろいろを定義している
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



