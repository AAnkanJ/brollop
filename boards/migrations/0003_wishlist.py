# Generated by Django 2.2.6 on 2019-12-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_topic_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
    ]