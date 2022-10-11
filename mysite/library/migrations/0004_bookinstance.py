# Generated by Django 4.1.1 on 2022-10-03 00:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')),
                ('due_back', models.DateField(blank=True, verbose_name='Bus prieinama')),
                ('status', models.CharField(blank=True, choices=[('a', 'Administruojama'), ('p', 'Paimta'), ('g', 'Galima paimti'), ('r', 'Rezervuota')], default='a', help_text='Statusas', max_length=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
            ],
        ),
    ]
