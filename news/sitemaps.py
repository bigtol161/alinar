from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Executor


class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at or obj.created_at

    def location(self, obj):
        return reverse('news:article_detail', args=[obj.slug])


class ExecutorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Executor.objects.all()

    def location(self, obj):
        return reverse('news:executor_detail', args=[obj.slug])


class StaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return ['news:article_list', 'news:executor_list']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'articles': ArticleSitemap,
    'executors': ExecutorSitemap,
    'static': StaticSitemap,
}
