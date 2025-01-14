from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



DATABASE_URL = 'postgresql://todoapplicationdatabase_bz6l_user:UI08095hltqURTWPA671ej8nhNCd5bFc@dpg-cu34b39opnds7381rm80-a/todoapplicationdatabase_bz6l'
# DATABASE_URL = 'mysql+pymysql://root:1bh14me027@127.0.0.1:3307/todoapplicationdatabase'


engine = create_engine(DATABASE_URL)
LocalSession = sessionmaker(bind=engine)
Base = declarative_base()