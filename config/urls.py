from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from news import views as news_views
from news.sitemaps import ArticleSitemap, ExecutorSitemap, StaticSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'executors': ExecutorSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', news_views.robots, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('news.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
]

# Оформление админки
from django.contrib import admin as _admin
_admin.site.site_header = 'Алинар — панель управления'
_admin.site.site_title = 'Алинар'
_admin.site.index_title = 'Управление сайтом'

# Оформление админки
from django.contrib import admin as _admin
_admin.site.site_header = 'Дом услуг — панель управления'
_admin.site.site_title = 'Дом услуг'
_admin.site.index_title = 'Управление сайтом'
