# Generated by Django 2.2.8 on 2020-03-26 10:54

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0004_auto_20200326_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=markdownx.models.MarkdownxField(verbose_name='答案内容'),
        ),
    ]
