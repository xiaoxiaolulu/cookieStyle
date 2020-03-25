# Generated by Django 2.2.8 on 2020-03-25 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.BooleanField(default=True, verbose_name='赞同或反对')),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes_on', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '投票',
                'verbose_name_plural': '投票',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='问题标题')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, verbose_name='(URL)别名')),
                ('content', models.TextField(verbose_name='问题内容')),
                ('has_correct', models.BooleanField(default=False, verbose_name='是否有正确回答')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('tags', taggit.managers.TaggableManager(help_text='多个标签使用, (英文)隔开', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='标签')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='提问者')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
                'ordering': ('-updated_at', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='答案内容')),
                ('is_accepted', models.BooleanField(default=False, verbose_name='是否被接受')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quora.Question', verbose_name='问题')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL, verbose_name='回答者')),
            ],
            options={
                'verbose_name': '答案',
                'verbose_name_plural': '答案',
                'ordering': ('-updated_at', '-created_at'),
            },
        ),
    ]