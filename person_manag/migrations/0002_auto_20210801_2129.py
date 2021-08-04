# Generated by Django 3.2.5 on 2021-08-01 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_manag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name_Group', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='FIO',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='Official',
            field=models.CharField(choices=[('1', 'Уборщик'), ('2', 'Охранник'), ('3', 'Кассир')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='activate_code',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='customuser',
            name='token_data',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='person_group',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='person_manag.groupperson'),
            preserve_default=False,
        ),
    ]