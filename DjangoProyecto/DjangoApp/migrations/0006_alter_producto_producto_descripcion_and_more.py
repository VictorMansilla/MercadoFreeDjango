# Generated by Django 5.0.6 on 2024-07-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoApp', '0005_rename_contraseña_usuario_usuario_contrasegna_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='producto_descripcion',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email_usuario',
            field=models.EmailField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono_usuario',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
