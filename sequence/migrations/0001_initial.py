# Generated by Django 2.2.2 on 2019-06-27 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tikee',
            fields=[
                ('tikee_id', models.CharField(max_length=24, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ShortSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('start', models.DateTimeField()),
                ('upload_to_cloud', models.BooleanField(default=True)),
                ('image_format', models.CharField(default='jpeg', max_length=10)),
                ('keep_local_copy', models.BooleanField(default=False)),
                ('sequence_id', models.BigIntegerField(default=0)),
                ('shooting_status', models.CharField(max_length=100, null=True)),
                ('nb_images_on_sd', models.IntegerField(default=0)),
                ('nb_images_uploaded', models.IntegerField(default=0)),
                ('interval', models.IntegerField(default=10)),
                ('duration', models.IntegerField(default=86400)),
                ('tikee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequence.Tikee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LongSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('start', models.DateTimeField()),
                ('upload_to_cloud', models.BooleanField(default=True)),
                ('image_format', models.CharField(default='jpeg', max_length=10)),
                ('keep_local_copy', models.BooleanField(default=False)),
                ('sequence_id', models.BigIntegerField(default=0)),
                ('shooting_status', models.CharField(max_length=100, null=True)),
                ('nb_images_on_sd', models.IntegerField(default=0)),
                ('nb_images_uploaded', models.IntegerField(default=0)),
                ('infinite_duration', models.BooleanField(default=False)),
                ('end', models.DateTimeField()),
                ('tikee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequence.Tikee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
