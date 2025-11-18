from django.contrib import admin

from .models import ConstructionModel, ModelAttachment


class ModelAttachmentInline(admin.TabularInline):
    model = ModelAttachment
    extra = 0
    readonly_fields = ['file', 'is_plan', 'uploaded_at']


@admin.register(ConstructionModel)
class ConstructionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'created_at']
    search_fields = ['name', 'user__username', 'user__rut']
    list_filter = ['status', 'created_at']
    inlines = [ModelAttachmentInline]
