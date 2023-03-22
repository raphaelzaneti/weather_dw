from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from local_settings import postgresql_credentials as psettings

# Database utils setup

def get_engine():
    url = f"postgresql://{psettings['pg_user']}:{psettings['pg_password']}@{psettings['pg_host']}:{psettings['pg_port']}/{psettings['pg_db']}"
    engine = create_engine(url, pool_size=50, echo=False)
    print(engine.url)
    return engine

def get_section():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session
