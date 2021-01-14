from django.contrib import admin
from defence.models import Category, Post, Comment, Contact, VideoItem, AboutCompany
# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,AdminCategory)

class AdminPost(admin.ModelAdmin):
    list_display=['title','slug','user','created','updated','publish','status']
    list_filter=('status','user','publish',)
    search_fields=('title','body',)
    date_hierarchy='publish'
    ordering=['status','publish']
    prepopulated_fields={'slug':('title',)}


admin.site.register(Post,AdminPost)


class AdminContact(admin.ModelAdmin):
    list_display=['id','name','email','phone','body']
admin.site.register(Contact,AdminContact)


admin.site.register(VideoItem,)

admin.site.register(AboutCompany)

class AdminComment(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated']
    list_filter=('active','created','body')
    search_fields=('name','email','body')

admin.site.register(Comment,AdminComment)