from django.urls import path

urlpatterns = [
    path('', ArticleListView.as_view(), name='wiki_article_index'),
    path('article/<str:slug>', ArticleDetailView.as_view(), name='wiki_article_detail'),
    path('history/<str:slug>', ArticleHistoryView.as_view(), name='wiki_article_history'),
    path('add/article',add_article, name='wiki_article_add'),
    path('edit/article/<str:slug>', edit_article, name='wiki_article_edit'),

]