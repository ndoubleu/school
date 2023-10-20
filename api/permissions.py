from rest_framework import permissions

class IsReportGroupAccessAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous:
            return request.user.is_director or (request.user.is_teacher and request.user.group == view.group)
        else: return False
    
class isSelfReportAccessAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous:
            return request.user.is_student
        else: return False