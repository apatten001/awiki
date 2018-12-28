from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(is_published=True)


class Article(models.Model):
    """
    This represents a wiki article

    """

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    text = models.TextField(help_text='Formatted using ReST')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, verbose_name='Published?')
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    published = PublishedArticleManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return 'wiki_article_detail', (), {'slug': self.slug}


class Edit(models.Model):

    """
    This stores an edit session
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_on = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=100)

    class Meta:
        ordering = ['-edited_on']

    def __str__(self):
        return "%s - %s - %s" % (self.summary, self.editor, self.edited_on)

    def get_absolute_url(self):
        return 'wiki_edit_detail', self.id






