"""
Authorization module for OpenHands.

This module provides permission-based authorization for API endpoints.
In OSS mode, all authorization checks pass (no-op).
In SAAS mode, the enterprise implementation performs real authorization checks.
"""

from openhands.server.auth.authorization import (
    ROLE_PERMISSIONS,
    Permission,
    RoleName,
    get_role_permissions,
    has_permission,
    require_org_admin,
    require_org_owner,
    require_org_role,
    require_org_user,
    require_permission,
)

__all__ = [
    'Permission',
    'RoleName',
    'ROLE_PERMISSIONS',
    'get_role_permissions',
    'has_permission',
    'require_permission',
    'require_org_role',
    'require_org_user',
    'require_org_admin',
    'require_org_owner',
]
