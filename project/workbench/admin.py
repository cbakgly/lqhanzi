# -*- coding:utf8 -*-
from django.contrib import admin
from models import Diaries, Tag, Credits, CreditSort


# Register your models here.


class DiaryAdmin(admin.ModelAdmin):
    list_display = ("user", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)


class CreditsAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit', 'sort')


class CreditSortAdmin(admin.ModelAdmin):
    list_display = ('credit_sort',)


admin.site.register(Diaries, DiaryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Credits, CreditsAdmin)
admin.site.register(CreditSort, CreditSortAdmin)
