from django.contrib import admin
from .models import User, Post


# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         "username",
#         "id",
#         "posts",
#     )


# Register your models here.
# admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
admin.site.register(Post)
