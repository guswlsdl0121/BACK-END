# Generated by Django 3.2.13 on 2022-06-02 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('body', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
