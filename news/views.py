# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.core.paginator import Paginator

from .models import Post
from .filters import NewsFilter
from .forms import PostForm

from datetime import datetime


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['length'] = Post.objects.count()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class SearchNews(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news_search'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    template_name = 'news/news_detail.html'
    queryset = Post.objects.all()


class AddNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/news_add.html'
    context_object_name = 'news_add'
    form_class = PostForm


class UpdateNews(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/news_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/'
