# Generated by Django 4.1.4 on 2023-01-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='province',
            field=models.CharField(choices=[('lumbini', 'lumbini'), ('madesh', 'madesh'), ('gagmati', 'bagmati'), ('gandaki', 'gandaki'), ('karnali', 'karnali'), ('sudur paschim', 'sudur paschim'), ('province no 1', 'province no 1')], max_length=100, verbose_name='province'),
        ),
    ]