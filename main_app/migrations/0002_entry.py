# Generated by Django 3.2.7 on 2021-09-18 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Entry Date')),
                ('episode', models.IntegerField(default=1)),
                ('season', models.IntegerField(default=1)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.content')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]