from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
#from sqlalchemy.orm import declarative_base

database_url = "sqlite:///mydb.db"
# database_url = "postgresql://user:password@host:port/db_name"

engine = create_engine(database_url,echo=False)


Base = declarative_base()

#Base.metadata.create_all(bind=engine)

# For connecting to postgres db on testing server 
# postgresql_db_user = 'postgres'
# postgresql_db_password = 'kp@123'
# host_server = '138.68.77.85'
# db_server_port = 5434
# ssl_mode = 'prefer'
# db_name = 'mydb'
# database_url = f'postgresql://{postgresql_db_user}:{quote(postgresql_db_password)}@' \
#                 f'{host_server}:{db_server_port}/{db_name}?sslmode={ssl_mode}'
# engine = create_engine(database_url, echo=False, pool_size=2, max_overflow=0, pool_recycle=3600,
#                             pool_pre_ping=True)

Sessionlocal = sessionmaker(engine)