from django.contrib import admin
from .models import Post,Contact,Profile
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display=['id','title','desc']

@admin.register(Contact)
class PostAdmin(admin.ModelAdmin):
  list_display=['name','email','address','message']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','token','verify']