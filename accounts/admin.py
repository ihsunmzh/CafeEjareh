from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# --- Added My Extra Personal Info --- 
UserAdmin.fieldsets[1][1]['fields'] = (  
										'email',
										'mobile_number',
										'home_phone_number',
										'birthdate',
										'home_address', 
										'state', 
										'city', 
										'bio', 
									)


# --- Added My Extra Permissions --- 
UserAdmin.fieldsets[2][1]['fields'] = (
										'is_active', 
										'is_staff', 
										'is_superuser', 
										'is_author', 
										'is_block', 
										'special_user', 
										'groups', 
										'user_permissions',
									)


UserAdmin.fieldsets += (
	("تصویر پروفایل", {
		"fields": (
			'avatar',
		),
	}),
)


# Action For Block User -->
def make_block(self, request, queryset):
		queryset.update(is_author=True)

make_block.short_description = "بلاک کردن کاربر"

# Action For UnBlock User -->
def make_unblock(self, request, queryset):
		queryset.update(is_author=False)

make_unblock.short_description = "خارج کردن از بلاک"

UserAdmin.actions += [make_block, make_unblock, ]


UserAdmin.ordering = ('-date_joined',)
UserAdmin.list_display += ('is_author', 'is_special_user', 'is_block')

admin.site.register(User, UserAdmin),

