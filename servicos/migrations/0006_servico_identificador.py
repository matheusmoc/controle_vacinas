# Generated by Django 4.1.7 on 2023-04-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0005_servico_finalizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='identificador',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
