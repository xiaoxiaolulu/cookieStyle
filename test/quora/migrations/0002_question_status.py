# Generated by Django 2.2.8 on 2020-03-25 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('C', 'Close'), ('D', 'Draft')], default='0', max_length=1, verbose_name='问题状态'),
        ),
    ]
