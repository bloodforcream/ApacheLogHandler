# Generated by Django 3.1.1 on 2020-09-24 17:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApacheLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес лога')),
                ('log_date', models.DateTimeField(verbose_name='Дата лога')),
                ('http_method', models.CharField(max_length=10, verbose_name='Метод лога')),
                ('uri', models.URLField(max_length=1024, verbose_name='URI лога')),
                ('status_code', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(599)], verbose_name='Статус код лога')),
                ('response_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='Размер ответа')),
            ],
        ),
    ]