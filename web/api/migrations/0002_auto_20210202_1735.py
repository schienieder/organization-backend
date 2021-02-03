# Generated by Django 3.1.5 on 2021-02-02 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badges',
            options={'ordering': ['-date_received']},
        ),
        migrations.AlterModelOptions(
            name='currentuserplan',
            options={'ordering': ['-expiration_date']},
        ),
        migrations.AlterModelOptions(
            name='paymentplans',
            options={'ordering': ['-amount']},
        ),
        migrations.AlterModelOptions(
            name='userauth',
            options={'ordering': ['-expiration']},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'ordering': ['-year_level']},
        ),
        migrations.AddIndex(
            model_name='userauth',
            index=models.Index(fields=['one_time_code'], name='user_otc'),
        ),
        migrations.AddIndex(
            model_name='userinfo',
            index=models.Index(fields=['year_level'], name='stud_year_level'),
        ),
    ]
