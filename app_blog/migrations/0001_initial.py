# Generated by Django 4.2.3 on 2023-08-05 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posteo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=64)),
                ('bajada', models.CharField(max_length=140)),
                ('imagen', models.ImageField(upload_to='media')),
                ('texto', models.CharField(max_length=5000)),
                ('fecha_publicacion', models.DateField(null=True)),
                ('creador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posteo_creados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
