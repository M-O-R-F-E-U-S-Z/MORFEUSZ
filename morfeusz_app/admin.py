from django.contrib import admin
from morfeusz_app.models import Movie, Group
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = ['title']
    search_fields = ['title']
    readonly_fields = ['title']

    class Meta:
        model = Movie


admin.site.register(Movie, MovieAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']
    search_fields = ['name']

    class Meta:
        model = Group


admin.site.register(Group, GroupAdmin)