# -*- coding:utf8 -*-
from django.contrib import admin
from models import Diaries,Tag
# Register your models here.


class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user_id", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)


admin.site.register(Diaries, DiaryAdmin)
admin.site.register(Tag, TagAdmin)
