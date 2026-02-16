"""
Permission-based authorization for API endpoints (OSS/OpenHands mode).

This module provides no-op authorization dependencies that always allow access.
In OSS mode, all users are treated as having full permissions.

For SAAS mode with real authorization checks, see the enterprise implementation
which overrides these no-op dependencies with actual permission validation.

Usage:
    from openhands.server.auth import (
        Permission,
        require_permission,
        require_org_role,
        require_org_user,
        require_org_admin,
        require_org_owner,
    )

    @router.get('/{org_id}/settings')
    async def get_settings(
        org_id: UUID,
        user_id: str = Depends(require_permission(Permission.VIEW_LLM_SETTINGS)),
    ):
        # In OSS mode, this always passes
        # In SAAS mode, this checks actual permissions
        ...
"""

from enum import Enum
from uuid import UUID

from fastapi import Depends

from openhands.server.user_auth import get_user_id


class Permission(str, Enum):
    """Permissions that can be assigned to roles."""

    # Secrets
    MANAGE_SECRETS = 'manage_secrets'

    # MCP
    MANAGE_MCP = 'manage_mcp'

    # Integrations
    MANAGE_INTEGRATIONS = 'manage_integrations'

    # Application Settings
    MANAGE_APPLICATION_SETTINGS = 'manage_application_settings'

    # API Keys
    MANAGE_API_KEYS = 'manage_api_keys'

    # LLM Settings
    VIEW_LLM_SETTINGS = 'view_llm_settings'
    EDIT_LLM_SETTINGS = 'edit_llm_settings'

    # Billing
    VIEW_BILLING = 'view_billing'
    ADD_CREDITS = 'add_credits'

    # Organization Members
    INVITE_USER_TO_ORGANIZATION = 'invite_user_to_organization'
    CHANGE_USER_ROLE_MEMBER = 'change_user_role:member'
    CHANGE_USER_ROLE_ADMIN = 'change_user_role:admin'
    CHANGE_USER_ROLE_OWNER = 'change_user_role:owner'

    # Organization Management
    CHANGE_ORGANIZATION_NAME = 'change_organization_name'
    DELETE_ORGANIZATION = 'delete_organization'


class RoleName(str, Enum):
    """Role names used in the system."""

    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'


# Permission mappings for each role
# In OSS mode, these are defined for consistency but not enforced
ROLE_PERMISSIONS: dict[RoleName, frozenset[Permission]] = {
    RoleName.OWNER: frozenset(
        [
            # Settings (Full access)
            Permission.MANAGE_SECRETS,
            Permission.MANAGE_MCP,
            Permission.MANAGE_INTEGRATIONS,
            Permission.MANAGE_APPLICATION_SETTINGS,
            Permission.MANAGE_API_KEYS,
            Permission.VIEW_LLM_SETTINGS,
            Permission.EDIT_LLM_SETTINGS,
            Permission.VIEW_BILLING,
            Permission.ADD_CREDITS,
            # Organization Members
            Permission.INVITE_USER_TO_ORGANIZATION,
            Permission.CHANGE_USER_ROLE_MEMBER,
            Permission.CHANGE_USER_ROLE_ADMIN,
            Permission.CHANGE_USER_ROLE_OWNER,
            # Organization Management (Owner only)
            Permission.CHANGE_ORGANIZATION_NAME,
            Permission.DELETE_ORGANIZATION,
        ]
    ),
    RoleName.ADMIN: frozenset(
        [
            # Settings (Full access)
            Permission.MANAGE_SECRETS,
            Permission.MANAGE_MCP,
            Permission.MANAGE_INTEGRATIONS,
            Permission.MANAGE_APPLICATION_SETTINGS,
            Permission.MANAGE_API_KEYS,
            Permission.VIEW_LLM_SETTINGS,
            Permission.EDIT_LLM_SETTINGS,
            Permission.VIEW_BILLING,
            Permission.ADD_CREDITS,
            # Organization Members
            Permission.INVITE_USER_TO_ORGANIZATION,
            Permission.CHANGE_USER_ROLE_MEMBER,
            Permission.CHANGE_USER_ROLE_ADMIN,
        ]
    ),
    RoleName.MEMBER: frozenset(
        [
            # Settings (Full access)
            Permission.MANAGE_SECRETS,
            Permission.MANAGE_MCP,
            Permission.MANAGE_INTEGRATIONS,
            Permission.MANAGE_APPLICATION_SETTINGS,
            Permission.MANAGE_API_KEYS,
            # LLM Settings (View only)
            Permission.VIEW_LLM_SETTINGS,
        ]
    ),
}


def get_role_permissions(role_name: str) -> frozenset[Permission]:
    """
    Get the permissions for a role.

    Args:
        role_name: Name of the role

    Returns:
        Set of permissions for the role
    """
    try:
        role_enum = RoleName(role_name)
        return ROLE_PERMISSIONS.get(role_enum, frozenset())
    except ValueError:
        return frozenset()


def has_permission(role_name: str, permission: Permission) -> bool:
    """
    Check if a role has a specific permission.

    In OSS mode, this always returns True (no-op).

    Args:
        role_name: Name of the role
        permission: Permission to check

    Returns:
        True (always in OSS mode)
    """
    return True


def require_permission(permission: Permission):
    """
    Factory function that creates a no-op dependency for permission checks.

    In OSS mode, this always allows access and returns the user_id.
    In SAAS mode, the enterprise implementation overrides this with real checks.

    Usage:
        @router.get('/{org_id}/settings')
        async def get_settings(
            org_id: UUID,
            user_id: str = Depends(require_permission(Permission.VIEW_LLM_SETTINGS)),
        ):
            ...

    Args:
        permission: The permission required (ignored in OSS mode)

    Returns:
        Dependency function that returns user_id
    """

    async def permission_checker(
        org_id: UUID,
        user_id: str | None = Depends(get_user_id),
    ) -> str | None:
        # In OSS mode, no permission check is performed
        return user_id

    return permission_checker


def require_org_role(required_role_name: str):
    """
    Factory function that creates a no-op dependency for role checks.

    In OSS mode, this always allows access and returns the user_id.
    In SAAS mode, the enterprise implementation overrides this with real checks.

    Usage:
        @router.get('/{org_id}/resource')
        async def get_resource(
            org_id: UUID,
            user_id: str = Depends(require_org_role('user')),
        ):
            ...

    Args:
        required_role_name: Name of the minimum required role (ignored in OSS mode)

    Returns:
        Dependency function that returns user_id
    """

    async def role_checker(
        org_id: UUID,
        user_id: str | None = Depends(get_user_id),
    ) -> str | None:
        # In OSS mode, no role check is performed
        return user_id

    return role_checker


# Convenience dependencies for common role checks (no-op in OSS mode)
require_org_user = require_org_role('user')
require_org_admin = require_org_role('admin')
require_org_owner = require_org_role('owner')
