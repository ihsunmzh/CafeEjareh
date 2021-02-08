from django.contrib import admin
from mysite.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'text')


admin.site.site_header = "پنل مدیریت رنت کالا"
admin.site.site_title = "پنل مدیریت رنت کالا"
admin.site.index_title = "به پنل مدیریت رنت کالا خوش آمدید!"