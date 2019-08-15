# Generated by Django 2.1.2 on 2019-08-05 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0016_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='id',
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='schedule_blob',
            unique_together={('day', 'start_time', 'end_time', 'user', 'semester')},
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('user', 'start_date', 'end_date')},
        ),
    ]