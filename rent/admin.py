from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from rent.models import (
	Category,
	City,
	Comment,
	Images,
	Rent,
	State,
)

admin.site.register(Category , MPTTModelAdmin) 
admin.site.register(City)
admin.site.register(Images)
admin.site.register(State)


class CommentInline(admin.TabularInline):
	model = Comment


class ImagesInline(admin.TabularInline):
	model = Images


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('fullname', 'comment_text', 'created_at', 'active')
	list_filter = ('active', 'created_at')
	search_fields = ('fullname', 'comment_text')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)

	approve_comments.short_description = "انتشار دیدگاه های انتخاب شده"
	


# My Actions For Rent Ads
def make_published(modeladmin, request, queryset):
	rows_updated = queryset.update(status='p')
	if rows_updated == 1:
		message_bit = "منتشر شد."
	else:
		message_bit = "منتشر شدند."
	modeladmin.message_user(request, "{} آگهی {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار آگهی های انتخاب شده"

def make_draft(modeladmin, request, queryset):
	rows_updated = queryset.update(status='d')
	if rows_updated == 1:
		message_bit = "پیش‌نویس شد."
	else:
		message_bit = "پیش‌نویس شدند."
	modeladmin.message_user(request, "{} آگهی {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش‌نویس شدن آگهی های انتخاب شده"

def make_reject(modeladmin, request, queryset):
	rows_updated = queryset.update(status='b')
	if rows_updated == 1:
		message_bit = "رد شد."
	else:
		message_bit = " رد شدند."
	modeladmin.message_user(request, "{} آگهی {}".format(rows_updated, message_bit))
make_reject.short_description = "رد کردن آگهی های انتخاب شده"

@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_at', 'status')
	inlines = [CommentInline, ImagesInline]
	actions = [make_published, make_draft, make_reject]