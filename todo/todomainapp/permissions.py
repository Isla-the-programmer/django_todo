from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'creator':
            return True
        elif request.user.is_authenticated and request.user.role == 'completer' and request.method in ['GET', 'PATCH']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'creator':
            return True
        elif view.action == 'partial_update' and request.user.role == 'completer':
            return request.data.get('completed') is not None
        elif view.action == 'retrieve' and request.user.role == 'completer':
            return True
        else:
            return False

