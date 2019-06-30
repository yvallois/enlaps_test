# Generated by Django 2.2.2 on 2019-06-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sequence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='XRequestId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
