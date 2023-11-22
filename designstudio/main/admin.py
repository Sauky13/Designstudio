from django.contrib import admin
from .models import AdvUser, Category, Application

admin.site.register(AdvUser)
admin.site.register(Category)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description', 'category', 'image','time_mark','status','user')


