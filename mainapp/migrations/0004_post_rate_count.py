# Generated by Django 4.2.6 on 2023-10-25 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_post_rate_followship'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rate_count',
            field=models.IntegerField(default=0),
        ),
    ]
