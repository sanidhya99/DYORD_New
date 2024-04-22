from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    list_display = ('email', 'name','number','id','is_superuser',)
    list_filter = ('is_superuser',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')},),
        ('Personal info', {'fields': ('name','number')},),
        ('Permissions', {'fields': ('is_superuser',)},),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('email', 'name','number','password1', 'password2'),
            },
        ),
    )
    search_fields = ('email','name',)
    ordering = ('email','id')
    filter_horizontal = ()


admin.site.register(CustomUser,UserModelAdmin)

# Register your models here.
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    list_display = ('id','email', 'name','number','is_superuser',)
    list_filter = ('is_superuser',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')},),
        ('Personal info', {'fields': ('name','number','people',)},),
        ('Permissions', {'fields': ('is_superuser',)},),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('email', 'name','number','password1', 'password2'),
            },
        ),
    )
    search_fields = ('email','name',)
    ordering = ('email','id')
    filter_horizontal = ()


# admin.site.register(CustomUser,UserModelAdmin)


