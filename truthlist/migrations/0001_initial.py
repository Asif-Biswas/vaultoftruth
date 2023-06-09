# Generated by Django 4.2.1 on 2023-05-21 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='initialquestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('question', models.CharField(max_length=255, verbose_name='Question')),
            ],
        ),
        migrations.CreateModel(
            name='number',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255, verbose_name='Answer')),
            ],
        ),
        migrations.CreateModel(
            name='quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Number')),
                ('question', models.CharField(max_length=255, verbose_name='Question')),
            ],
        ),
    ]
