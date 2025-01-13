from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



DATABASE_URL = 'postgresql://postgres:1bh14me027@localhost/TodoApplicationDatabase'
# DATABASE_URL = 'mysql+pymysql://root:1bh14me027@127.0.0.1:3307/todoapplicationdatabase'


engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()