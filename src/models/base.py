from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

def get_base(schema: str):
    """Return a SQLAlchemy Base class bound to a specific schema."""
    metadata = MetaData(schema=schema)
    Base = declarative_base(metadata=metadata)
    return Base
