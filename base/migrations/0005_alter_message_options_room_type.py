# Generated by Django 4.2.5 on 2023-09-16 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
