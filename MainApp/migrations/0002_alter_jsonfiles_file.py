# Generated by Django 4.2.5 on 2023-09-05 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsonfiles',
            name='file',
            field=models.FileField(upload_to='json_files/'),
        ),
    ]
