"""Publish automation events and notify listeners via PostgreSQL NOTIFY."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session
from storage.automation_event import AutomationEvent


def publish_automation_event(
    session: Session,
    source_type: str,
    payload: dict,
    dedup_key: str,
    metadata: dict | None = None,
) -> AutomationEvent:
    """Create an :class:`AutomationEvent` and add it to the session.

    The caller is responsible for committing (or flushing) the session.
    """
    event = AutomationEvent(
        source_type=source_type,
        payload=payload,
        dedup_key=dedup_key,
        metadata_=metadata,
    )
    session.add(event)
    return event


def pg_notify_new_event(session: Session, event_id: int) -> None:
    """Send a PostgreSQL ``NOTIFY`` on the ``automation_events`` channel."""
    session.execute(
        text("SELECT pg_notify('automation_events', :event_id)"),
        {'event_id': str(event_id)},
    )
