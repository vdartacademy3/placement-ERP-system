from rest_framework.permissions import BasePermission

from apps.accounts.models import User


class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.SUPER_ADMIN
        )


class IsCollegeAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.COLLEGE_ADMIN
        )


class IsHOD(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.HOD
        )


class IsFaculty(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.FACULTY
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.STUDENT
        )


class IsAccountant(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ACCOUNTANT
        )


class IsLibrarian(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.LIBRARIAN
        )


class IsSuperAdminOrCollegeAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.SUPER_ADMIN,
                User.Role.COLLEGE_ADMIN,
            ]
        )


class IsFacultyOrHOD(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.FACULTY,
                User.Role.HOD,
            ]
        )


class IsStaffMember(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.SUPER_ADMIN,
                User.Role.COLLEGE_ADMIN,
                User.Role.HOD,
                User.Role.FACULTY,
                User.Role.ACCOUNTANT,
                User.Role.LIBRARIAN,
            ]
        )