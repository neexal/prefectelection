# Generated by Django 5.0.2 on 2025-05-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_candidate_position_remove_voter_selected_stalls_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(default='1', upload_to='candidates/'),
            preserve_default=False,
        ),
    ]
