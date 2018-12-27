from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .models import Edit, Article
from .forms import ArticleForm, EditArticleForm

# Create your views here.


@login_required
def add_article(request):
    """
    Allows a logged in user to add an article

    """

    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        msg = 'Article was saved successfully.'
        messages.success(request, msg, fail_silently=True)
        return redirect(article)
    return render(request, 'article/article_form.html', {'form': form})


@login_required
def edit_article(request, slug):
   """
   allows a logged in user to edit an article
   """
    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    edit_form = EditArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        if edit_form.is_valid():
            edit = edit_form.save(commit=False)
            edit.article = article
            edit.editor = request.user
            edit.save()
            msg = 'Article was edited successfully.'
            messages.success(request, msg, fail_silently=True)
            return redirect(article)
    return render(request, 'article/article_form.html', {'form': form, 'edit_form': edit_form})


def article_history(request, slug):
    """
    outputs the articles edit history
    """

    article = get_object_or_404(Article, slug=slug)
    queryset = Edit.objects.filter(article__slug=slug)
    return render(request, 'article/edit_list.html', {'article': article, 'queryset':queryset})


class ArticleList(ListView):
    """
    Gives the complete list of articles
     """
    template_name = 'article/article_list.html'

    def get_queryset(self):
        Article.objects.all()


class ArticleDetail(DetailView):
    """
    Gives a detail view of an article
    """
    model = Article
    template_name = 'article/article_detail.html'






