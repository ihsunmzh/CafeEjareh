from django.contrib import admin
from blog.models import Article, Category


def make_published(modeladmin, request, queryset):
		rows_updated = queryset.update(status='p')
		if rows_updated == 1:
			message_bit = "منتشر شد."
		else:
			message_bit = "منتشر شدند."
		modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار مقالات انتخاب شده"


def make_draft(modeladmin, request, queryset):
		rows_updated = queryset.update(status='d')
		if rows_updated == 1:
			message_bit = "پیش‌نویس شد."
		else:
			message_bit = "پیش‌نویس شدند."
		modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش‌نویس شدن مقالات انتخاب شده"


class ArticleAdmin(admin.ModelAdmin):
	# list_display = ('title', 'thumbnail_tag','slug', 'author', 'created_at', 'status', 'category_to_str')
	list_display = ('title', 'thumbnail_tag','slug', 'author', 'created_at', 'status',)
	list_filter = ('created_at','status', 'author')
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}
	ordering = ['-status', '-created_at']
	actions = [make_published, make_draft]

	def get_changeform_initial_data(self, request):
		get_data = super(ArticleAdmin, self).get_changeform_initial_data(request)
		get_data['author'] = request.user.pk
		return get_data

admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','slug', 'parent','status')
	list_filter = (['status'])
	search_fields = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


