from django.contrib import admin
from django.db.models import Count

from .models import City, Service


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'articles_count', 'executors_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(
                n_articles=Count('articles', distinct=True),
                n_executors=Count('executors', distinct=True),
            )
        )

    @admin.display(description='Статей', ordering='n_articles')
    def articles_count(self, obj):
        return obj.n_articles

    @admin.display(description='Мастеров', ordering='n_executors')
    def executors_count(self, obj):
        return obj.n_executors


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'articles_count', 'executors_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(
                n_articles=Count('articles', distinct=True),
                n_executors=Count('executors', distinct=True),
            )
        )

    @admin.display(description='Статей', ordering='n_articles')
    def articles_count(self, obj):
        return obj.n_articles

    @admin.display(description='Мастеров', ordering='n_executors')
    def executors_count(self, obj):
        return obj.n_executors
