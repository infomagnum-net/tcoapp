from django.contrib import admin

# Register your models here.
from .models import Comments
from django.db.models import TextField
class CommentAdmin(admin.ModelAdmin):
 	model=Comments

admin.site.register(Comments,CommentAdmin)

