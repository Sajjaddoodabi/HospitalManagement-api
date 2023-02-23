from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotAuthenticated(BasePermission):
    pass


class UserObjectOwner(BasePermission):
    pass


class IsAdmin(BasePermission):
    pass


class IsPatient(BasePermission):
    pass


class IsDoctor(BasePermission):
    pass


class IsDoctorDenied(BasePermission):
    pass
