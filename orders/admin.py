from django.contrib import admin
from django.utils.html import format_html

from .models import Order, Response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'city', 'service', 'budget', 'contact_name', 'phone', 'colored_status', 'author', 'created_at')
    list_filter = ('status', 'city', 'service')
    search_fields = ('number', 'title', 'description', 'contact_name', 'phone')
    readonly_fields = ('created_at',)
    list_per_page = 30

    @admin.display(description='Статус', ordering='status')
    def colored_status(self, obj):
        colors = {
            'new': '#b45309',
            'in_progress': '#1d4ed8',
            'done': '#15803d',
            'closed': '#6b7280',
        }
        return format_html(
            '<span style="color: {}; font-weight: 600;">{}</span>',
            colors.get(obj.status, '#374151'),
            obj.get_status_display(),
        )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('order', 'executor', 'price', 'created_at')
    list_filter = ('executor__city',)
    search_fields = ('order__title', 'executor__name', 'message')
    readonly_fields = ('created_at',)
    list_per_page = 30
