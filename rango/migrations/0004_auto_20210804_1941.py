# Generated by Django 2.2 on 2021-08-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20210804_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='Stars',
            field=models.IntegerField(verbose_name=(1, 2, 3, 4)),
        ),
    ]
