# Generated by Django 4.0.6 on 2022-07-15 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
    ]
