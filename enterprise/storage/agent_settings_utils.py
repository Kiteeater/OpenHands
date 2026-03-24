from __future__ import annotations

from typing import Any, Mapping

from storage.org import Org
from storage.org_member import OrgMember

_SCHEMA_VERSION = 1
_ORG_LEGACY_AGENT_SETTING_COLUMNS = {
    'agent': 'agent',
    'llm.model': 'default_llm_model',
    'llm.base_url': 'default_llm_base_url',
    'verification.confirmation_mode': 'confirmation_mode',
    'verification.security_analyzer': 'security_analyzer',
    'condenser.enabled': 'enable_default_condenser',
    'condenser.max_size': 'condenser_max_size',
    'max_iterations': 'default_max_iterations',
    'mcp_config': 'mcp_config',
}


def ensure_schema_version(agent_settings: Mapping[str, Any] | None) -> dict[str, Any]:
    normalized = dict(agent_settings or {})
    if normalized and 'schema_version' not in normalized:
        normalized['schema_version'] = _SCHEMA_VERSION
    return normalized


def merge_agent_settings(
    base: Mapping[str, Any] | None,
    updates: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged = dict(base or {})
    for key, value in (updates or {}).items():
        if key == 'schema_version':
            continue
        if value is None:
            merged.pop(key, None)
        else:
            merged[key] = value
    return ensure_schema_version(merged)


def get_org_agent_settings(org: Org) -> dict[str, Any]:
    agent_settings = dict(getattr(org, 'agent_settings', {}) or {})
    for key, column_name in _ORG_LEGACY_AGENT_SETTING_COLUMNS.items():
        if agent_settings.get(key) is not None:
            continue
        value = getattr(org, column_name, None)
        if value is not None:
            agent_settings[key] = value
    return ensure_schema_version(agent_settings)


def get_org_member_agent_settings(org_member: OrgMember) -> dict[str, Any]:
    return ensure_schema_version(dict(getattr(org_member, 'agent_settings', {}) or {}))
