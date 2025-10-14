from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Membership

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role']