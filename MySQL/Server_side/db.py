from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# ------------------------------------------------------------
# DATABASE URL (ASYNC MYSQL)
# ------------------------------------------------------------
DATABASE_URL = "mysql+aiomysql://apiuser:Ilovemygpu!1@localhost/dnd"

# ------------------------------------------------------------
# ASYNC ENGINE
# ------------------------------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# ------------------------------------------------------------
# SESSION FACTORY
# ------------------------------------------------------------
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# ------------------------------------------------------------
# BASE MODEL (for SQLAlchemy ORM models)
# ------------------------------------------------------------
Base = declarative_base()

# ------------------------------------------------------------
# DEPENDENCY FOR FASTAPI
# ------------------------------------------------------------
async def get_session():
    async with SessionLocal() as session:
        yield session