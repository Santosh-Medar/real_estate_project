from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Property

class CustomUserAdmin(UserAdmin):
    model = User

    # Show role column in list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

    # Display role while editing user
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )

    # Display role while creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)

# Register Property with custom list display
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'status')
    list_filter = ('status', 'seller')
    actions = ['approve_properties']

    def approve_properties(self, request, queryset):
        queryset.update(status='approved')