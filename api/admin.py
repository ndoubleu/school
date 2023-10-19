from django.contrib import admin
from django.http.request import HttpRequest
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'full_name')}),
        ('Permissions', {'fields': ('is_teacher', 'is_student', 'is_director', 'group','is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_teacher', 'is_student', 'is_director', 'group', 'is_active',),
        }),
    )
    list_display = ('username', 'is_teacher', 'is_student', 'is_director', 'group', 'is_active',)
    search_fields = ('username',)
    ordering = ('username',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_director:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_director:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_director:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_director:
            return True
        return False

class GroupAdmin(admin.ModelAdmin):
    list_display = ('group',)

    def get_queryset(self, request):
        queryset = super(GroupAdmin, self).get_queryset(request)
        if request.user.is_director:
            return queryset
        elif request.user.is_teacher:
            return queryset.filter(id=request.user.group.id)
        elif request.user.is_student:
            return queryset.filter(id=request.user.group.id)
        else:
            return queryset.none()
        
    def has_change_permission(self, request, obj=None):
        if obj and request.user.is_student or request.user.is_teacher:
            return False
        return super().has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        if request.user.is_student or request.user.is_teacher:
            return False
        return super().has_add_permission(request)
            
    def has_delete_permission(self, request, obj=None):
        if request.user.is_student or request.user.is_teacher:
            return False       
        return super().has_delete_permission(request, obj)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(group=request.user.group, is_student=True)
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.filter(group=request.user.group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super(GradeAdmin, self).get_queryset(request)
        if request.user.is_director:
            return queryset
        elif request.user.is_teacher:
           
            return queryset.filter(student__group=request.user.group)
        elif request.user.is_student:

            return queryset.filter(student=request.user)
        else:
            return queryset.none()

    def has_change_permission(self, request, obj=None):
        if obj and (request.user.is_student or request.user.is_teacher):

            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_teacher:
            return True
        if request.user.is_student:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_student or request.user.is_teacher:
            return False
        return super().has_delete_permission(request, obj)
    
admin.site.register(User)
admin.site.register(Group, GroupAdmin)
admin.site.register(Grade, GradeAdmin)

