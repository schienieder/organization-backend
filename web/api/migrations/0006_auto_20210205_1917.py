# Generated by Django 3.1.5 on 2021-02-05 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210203_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgapplication',
            name='date_accepted',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='orgapplication',
            name='decline_reason',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orgapplication',
            name='flagged',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='orgapplication',
            name='is_accepted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
