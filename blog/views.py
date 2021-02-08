from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView, ListView

from blog.models import Article


class ArticleView(ListView):
	model = Article
	template_name = 'weblog/blog.html'
	context_object_name = 'articles'
	paginate_by = 11


class ArticleDetailView(DetailView):
	template_name = 'weblog/blog-single-post.html'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Article.objects.published(), pk=pk)

	def get_context_data(self, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(**kwargs)
		context['latest_articles'] = Article.objects.all()[:4]
		return context