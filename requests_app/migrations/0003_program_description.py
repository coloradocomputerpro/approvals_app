# Generated by Django 3.2.18 on 2023-03-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_app', '0002_member_membertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
