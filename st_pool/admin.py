#encoding=utf-8
from django.contrib import admin

from models import *
class StockInfoAdmin(admin.ModelAdmin):



    list_display = ['pk', 'name', 'name']
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10
    # fields = ['bpub_date', 'btitle']
    fieldsets = [
        ('basic', {'fields': ['name']}),
        ('more', {'fields': ['name']}),
    ]


admin.site.register(StockInfo,StockInfoAdmin)


# class BookInfoAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'btitle', 'bpub_date']
#     list_filter = ['btitle']
#     search_fields = ['btitle']
#     list_per_page = 10
#     # fields = ['bpub_date', 'btitle']
#     fieldsets = [
#         ('basic', {'fields': ['btitle']}),
#         ('more', {'fields': ['bpub_date']}),
#     ]
#
#
# admin.site.register(BookInfo,BookInfoAdmin)
# admin.site.register(HeroInfo)