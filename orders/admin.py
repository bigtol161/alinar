from django.contrib import admin

from .models import Order, Response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'service', 'budget', 'contact_name', 'phone', 'status', 'author', 'created_at')
    list_filter = ('status', 'city', 'service')
    search_fields = ('title', 'description', 'contact_name', 'phone')
    readonly_fields = ('created_at',)
    list_per_page = 30


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('order', 'executor', 'price', 'created_at')
    list_filter = ('executor__city',)
    search_fields = ('order__title', 'executor__name', 'message')
    readonly_fields = ('created_at',)
    list_per_page = 30
