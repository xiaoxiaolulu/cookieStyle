# Generated by Django 2.2.8 on 2020-03-25 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20200324_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, verbose_name='文章标题'),
        ),
    ]