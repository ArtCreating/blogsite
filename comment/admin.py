from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class ComemntAdmin(admin.ModelAdmin):
   list_display = ('id', 'user', 'content_object', 'text', 'comment_time')