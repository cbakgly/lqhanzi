from rest_framework import permissions

from utils import has_workbench_perm


class IsBusinessMember(permissions.BasePermission):
    """
    Custom permission to only allow members of our business to edit it.
    """

    def has_permission(self, request, view):
        return has_workbench_perm(request.user)
