# Generated by Django 5.0.7 on 2024-07-26 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoApp', '0007_alter_usuario_nombre_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro_Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion_nombre', models.CharField(choices=[('agregar', 'Agregar'), ('borrar', 'Borrar'), ('editar', 'Editar')], default=None, max_length=10, null=True)),
                ('accion_usuario_id', models.IntegerField()),
                ('accion_usuario', models.CharField(max_length=200)),
                ('accion_producto_id', models.IntegerField()),
                ('accion_momento', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Registro_Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion_nombre', models.CharField(choices=[('agregar', 'Agregar'), ('borrar', 'Borrar'), ('editar', 'Editar')], default=None, max_length=10, null=True)),
                ('accion_usuario_id', models.IntegerField()),
                ('accion_usuario_nombre', models.CharField(max_length=200)),
                ('accion_momento', models.TimeField()),
            ],
        ),
    ]
