from django.contrib import admin

from datastore.models import Message, Link, User, Article, Frequent


class MessageAdmin(admin.ModelAdmin):
    list_display = ('full_text', 'label', 'is_confirmed')
    list_filter = ('label', 'is_confirmed')
    search_fields = ('full_text', 'normalized_text')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'label', 'message')
    list_filter = ('label', 'is_confirmed')


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'ip', 'latitude', 'longitude')
    search_fields = ('phone', 'ip', 'latitude', 'longitude')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'verified_by', 'label')


class FrequentAdmin(admin.ModelAdmin):
    list_display = ('normalized_text', 'count', 'location')


admin.site.register(Message, MessageAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Frequent, FrequentAdmin)
