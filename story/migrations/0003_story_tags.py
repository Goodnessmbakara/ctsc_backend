# Generated by Django 5.0.4 on 2024-05-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_story_is_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='tags',
            field=models.CharField(blank=True, choices=[('Interview', 'Interview'), ('Personal Growth', 'Personal Growth'), ('Culture', 'Culture')], max_length=50, null=True),
        ),
    ]