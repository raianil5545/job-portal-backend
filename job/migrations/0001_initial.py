# Generated by Django 4.1.4 on 2022-12-31 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=150, verbose_name='job  name')),
                ('job_category', models.CharField(max_length=150, verbose_name='job category')),
                ('job_level', models.CharField(max_length=150, verbose_name='job level')),
                ('no_of_vacancy', models.PositiveSmallIntegerField(verbose_name='no of vacancy')),
                ('employment_type', models.CharField(max_length=150, verbose_name='employment type')),
                ('street_address', models.CharField(max_length=150, verbose_name='street address')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('offered_salary', models.CharField(max_length=150, verbose_name='offered salary')),
                ('application_deadline', models.DateField(verbose_name='application deadline')),
                ('education_level', models.CharField(max_length=150, verbose_name='education level')),
                ('experience_level', models.CharField(max_length=100, verbose_name='years of experience')),
                ('skills_required', django_mysql.models.ListCharField(models.CharField(max_length=100), max_length=1111, size=10, verbose_name='skills required')),
                ('other_specifications', models.TextField(max_length=1500, verbose_name='other specifications')),
                ('job_description', models.TextField(max_length=2000, verbose_name='job description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
