from django.contrib import admin
from moodboard.models import Board, Image, Comment

class BoardAdmin(admin.ModelAdmin):
	list_display = ['name', 'description', 'pk']

class ImageAdmin(admin.ModelAdmin):
	list_display = ['name', 'url_external']

class CommentAdmin(admin.ModelAdmin):
	list_display = ['name', 'comment']

admin.site.register(Board, BoardAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)