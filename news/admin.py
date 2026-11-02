from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html

from .models import Article, Executor, Lead


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'rubric_display', 'city', 'service', 'status', 'published_at')
    list_display_links = ('title',)
    list_filter = ('rubric', 'city', 'service', 'is_published')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    list_per_page = 30
    actions = ('publish_articles', 'unpublish_articles')

    @admin.display(description='Рубрика', ordering='rubric')
    def rubric_display(self, obj):
        return obj.get_rubric_display()

    @admin.display(description='Опубл.', boolean=True, ordering='is_published')
    def status(self, obj):
        return obj.is_published

    @admin.action(description='Опубликовать выбранные статьи')
    def publish_articles(self, request, queryset):
        now = timezone.now()
        updated = 0
        for article in queryset:
            if not article.is_published:
                article.is_published = True
                if not article.published_at:
                    article.published_at = now
                article.save(update_fields=('is_published', 'published_at'))
                updated += 1
        self.message_user(request, f'Опубликовано статей: {updated}')

    @admin.action(description='Снять с публикации выбранные статьи')
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'Снято с публикации статей: {updated}')


@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'city', 'price_from', 'phone', 'is_active', 'leads_count', 'created_at')
    list_filter = ('city', 'services', 'is_active')
    search_fields = ('name', 'specialty', 'phone', 'description')
    fields = ('name', 'slug', 'specialty', 'city', 'services', 'photo', 'price_from', 'phone', 'description', 'user', 'is_active')
    filter_horizontal = ('services',)
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_leads=Count('leads'))

    @admin.display(description='Заявок', ordering='num_leads')
    def leads_count(self, obj):
        return obj.num_leads


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'executor', 'colored_status', 'created_at')
    list_filter = ('status', 'executor')
    list_editable = ('phone',)
    readonly_fields = ('created_at',)
    search_fields = ('name', 'phone', 'message')
    list_per_page = 30

    @admin.display(description='Статус', ordering='status')
    def colored_status(self, obj):
        colors = {'new': '#b45309', 'done': '#15803d'}
        return format_html(
            '<span style="color: {}; font-weight: 600;">{}</span>',
            colors.get(obj.status, '#374151'),
            obj.get_status_display(),
        )
