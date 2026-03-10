"""SQLAlchemy models for automations and automation runs.

Stub for Task 1 (Data Foundation). These models will be replaced when Task 1
is merged into automations-phase1.
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from storage.base import Base


class Automation(Base):
    __tablename__ = 'automations'

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    org_id = Column(String, nullable=True, index=True)

    name = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, server_default=text('true'))

    config = Column(JSON, nullable=False)
    trigger_type = Column(String, nullable=False)
    file_store_key = Column(String, nullable=False)

    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
    )

    runs = relationship('AutomationRun', back_populates='automation')


class AutomationRun(Base):
    __tablename__ = 'automation_runs'

    id = Column(String, primary_key=True)
    automation_id = Column(
        String, ForeignKey('automations.id', ondelete='CASCADE'), nullable=False
    )
    event_id = Column(Integer, ForeignKey('automation_events.id'), nullable=True)
    conversation_id = Column(String, nullable=True)
    status = Column(String, nullable=False, server_default=text("'PENDING'"))
    claimed_by = Column(String, nullable=True)
    claimed_at = Column(DateTime(timezone=True), nullable=True)
    heartbeat_at = Column(DateTime(timezone=True), nullable=True)
    retry_count = Column(Integer, nullable=False, server_default=text('0'))
    max_retries = Column(Integer, nullable=False, server_default=text('3'))
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    event_payload = Column(JSON, nullable=True)
    error_detail = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
    )

    automation = relationship('Automation', back_populates='runs')
