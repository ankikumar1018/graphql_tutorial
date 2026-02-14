from django.contrib import admin
from auth_app.models import UserProfile, Post, Comment, ActivityLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_email_verified', 'created_at']
    list_filter = ['role', 'is_email_verified', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['title', 'content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['text', 'author__username']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
