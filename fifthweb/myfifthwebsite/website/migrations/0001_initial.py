# Generated by Django 4.2 on 2023-04-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=1000, null=True)),
                ('content', models.TextField(blank=True, max_length=10000, null=True)),
                ('link_img', models.TextField(blank=True, max_length=10000, null=True)),
                ('url', models.TextField(blank=True, max_length=10000, null=True)),
                ('sign', models.CharField()),
            ],
            options={
                'db_table': 'admin',
            },
        ),
    ]
