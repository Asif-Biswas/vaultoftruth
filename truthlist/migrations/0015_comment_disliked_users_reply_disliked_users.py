# Generated by Django 4.2.1 on 2023-06-22 13:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('truthlist', '0014_comment_liked_users_reply_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='disliked_users',
            field=models.ManyToManyField(blank=True, related_name='disliked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reply',
            name='disliked_users',
            field=models.ManyToManyField(blank=True, related_name='disliked_replies', to=settings.AUTH_USER_MODEL),
        ),
    ]
