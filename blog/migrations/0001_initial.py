# Generated by Django 5.1.5 on 2025-02-02 17:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('cover', models.ImageField(blank=True, default='covers/default.png', upload_to='covers/', verbose_name='عکس جلد')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('views', models.IntegerField(default=0, verbose_name='بازدید')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_blogs', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.blog', verbose_name='وبلاگ')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comments', to='blog.comment', verbose_name='کامنت والد')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پاسخ')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_set', to='blog.comment', verbose_name='کامنت مربوطه')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_replies', to=settings.AUTH_USER_MODEL, verbose_name='لایک\u200cها')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]
