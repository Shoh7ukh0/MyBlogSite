# Generated by Django 5.0.1 on 2024-01-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_myabout_phone_alter_myabout_skils_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('location', models.CharField(max_length=250)),
                ('facebook', models.URLField()),
                ('instagram', models.URLField()),
                ('telegram', models.URLField()),
            ],
        ),
    ]