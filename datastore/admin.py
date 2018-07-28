from django.contrib import admin

from datastore.models import Message, Link, User


class MessageAdmin(admin.ModelAdmin):
    list_display = ('full_text', 'label', 'is_confirmed', 'sentiment_polarity', 'sentiment_subjectivity')
    list_filter = ('label', 'is_confirmed')
    search_fields = ('sentiment_polarity', 'sentiment_subjectivity', 'full_text')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'label', 'message')
    list_filter = ('label', 'is_confirmed')


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'ip', 'latitude', 'longitude')
    search_fields = ('phone', 'ip', 'latitude', 'longitude')


admin.site.register(Message, MessageAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(User, UserAdmin)
