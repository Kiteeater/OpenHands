"""SQLAlchemy model for automation events (the inbox).

Stub for Task 1 (Data Foundation). This model will be replaced when Task 1
is merged into automations-phase1.
"""

from sqlalchemy import Column, DateTime, Integer, String, Text, text
from sqlalchemy.types import JSON
from storage.base import Base


class AutomationEvent(Base):
    __tablename__ = 'automation_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    metadata_ = Column('metadata', JSON, nullable=True)
    dedup_key = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, server_default=text("'NEW'"))
    error_detail = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
    )
    processed_at = Column(DateTime(timezone=True), nullable=True)
