# Generated by Django 4.0.6 on 2023-05-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truthlist', '0002_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='initialquestions',
        ),
        migrations.DeleteModel(
            name='number',
        ),
        migrations.DeleteModel(
            name='quest',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
