# gestion/permissions.py

from rest_framework import permissions

def _is_in_group(user, group_name):
    """
    Toma un usuario y un nombre de grupo, y devuelve True si el usuario está en ese grupo.
    """
    return user.groups.filter(name=group_name).exists()

class EsAdministrador(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'Administrador')

class EsTecnico(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'Tecnico')

class EsRepositor(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'Repositor')