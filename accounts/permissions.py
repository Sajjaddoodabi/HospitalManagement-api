from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_anonymous


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class UserObjectOwner(BasePermission):
    pass


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        is_patient = True if request.user.role == 'PAT' else False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and is_patient)


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        is_doctor = True if request.user.role == 'DOC' else False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and is_doctor)


class IsDoctorDenied(BasePermission):
    pass
