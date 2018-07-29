from django.db import models

from backend.settings import (
    SHA256_LEN, PHONE_NUM_LEN, COORD_DIGITS,
    UNLABELLED_DEFAULT, COORD_DECIMAL, TITLE_LEN
)


class Message(models.Model):
    full_text = models.TextField()
    normalized_text = models.TextField()
    hash_value = models.CharField(max_length=SHA256_LEN, null=True)
    label = models.CharField(max_length=1, default=UNLABELLED_DEFAULT)

    is_real = models.BooleanField(default=False)
    is_trained = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True)


class Link(models.Model):
    message = models.ForeignKey(Message, null=True, on_delete=models.SET_NULL)
    url = models.URLField()
    label = models.CharField(max_length=1)

    is_trained = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True)


class User(models.Model):
    phone = models.CharField(max_length=PHONE_NUM_LEN, null=True)
    ip = models.GenericIPAddressField()
    latitude = models.DecimalField(max_digits=COORD_DIGITS, decimal_places=COORD_DECIMAL, null=True)
    longitude = models.DecimalField(max_digits=COORD_DIGITS, decimal_places=COORD_DECIMAL, null=True)

    messages = models.ManyToManyField(Message)


class Article(models.Model):
    title = models.CharField(max_length=TITLE_LEN)
    verified_by = models.TextField()
    content = models.URLField()

    users = models.ManyToManyField(User)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Frequent(models.Model):
    normalized_text = models.TextField()
    hash_value = models.CharField(max_length=SHA256_LEN, null=True)
    label = models.CharField(max_length=1, default=UNLABELLED_DEFAULT)
    count = models.IntegerField(default=0)
    location = models.CharField(max_length=TITLE_LEN)

    messages = models.ForeignKey(Message, null=True, on_delete=models.SET_NULL)
    article = models.OneToOneField(Article, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
